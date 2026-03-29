"""
TurkishVoice FastAPI - REST API Server

Endpoints:
- POST /api/v1/synthesize - Metin → Ses dönüştürme
- GET /api/v1/voices - Mevcut sesleri listele
- POST /api/v1/voices/clone - Ses klonlama
- GET /api/v1/health - Sağlık kontrolü
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
import tempfile
from pathlib import Path
import uuid
import asyncio

from turkishvoice import TurkishVoiceEngine

# Create FastAPI app
app = FastAPI(
    title="TurkishVoice API",
    description="Açık kaynak Türkçe Metin-Şarkı Sentezi API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
_engine: Optional[TurkishVoiceEngine] = None


def get_engine() -> TurkishVoiceEngine:
    """Get or create the global engine instance."""
    global _engine
    if _engine is None:
        _engine = TurkishVoiceEngine()
    return _engine


# Request/Response models
class SynthesisRequest(BaseModel):
    """Request model for speech synthesis."""
    text: str = Field(..., min_length=1, max_length=5000, description="Sentezlenecek Türkçe metin")
    voice: str = Field(default="default", description="Ses tanımlayıcısı")
    speed: float = Field(default=1.0, ge=0.5, le=2.0, description="Konuşma hızı")
    pitch: float = Field(default=1.0, ge=0.5, le=2.0, description="Perde çarpanı")
    prosody_scale: float = Field(default=1.0, ge=0.0, le=2.0, description="Dogaallık ölçeği")
    format: Literal["wav", "mp3", "ogg"] = Field(default="wav", description="Ses formatı")


class SynthesisResponse(BaseModel):
    """Response model for synthesis request."""
    audio_id: str
    status: str
    duration_seconds: float
    message: str


class VoiceInfo(BaseModel):
    """Voice information model."""
    id: str
    name: str
    gender: str
    age: str
    description: Optional[str] = None


class VoicesListResponse(BaseModel):
    """Response model for voices list."""
    voices: List[VoiceInfo]
    count: int


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    engine_loaded: bool


class BatchSynthesisRequest(BaseModel):
    """Request model for batch synthesis."""
    items: List[SynthesisRequest] = Field(..., max_items=1000)
    callback_url: Optional[str] = None


class BatchSynthesisResponse(BaseModel):
    """Response model for batch synthesis."""
    batch_id: str
    status: str
    total_items: int


class CloneRequest(BaseModel):
    """Request model for voice cloning."""
    voice_name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    language: Literal["tr", "mixed"] = "tr"


class CloneResponse(BaseModel):
    """Response model for voice cloning."""
    voice_id: str
    status: str
    message: str


# In-memory storage for audio files
_audio_storage: dict = {}


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    API sağlık kontrolü.

    Sunucunun çalışır durumda olduğunu doğrular.
    """
    engine = get_engine()
    return HealthResponse(
        status="ok",
        version="0.1.0",
        engine_loaded=engine.is_loaded,
    )


@app.post("/api/v1/synthesize", response_model=SynthesisResponse, tags=["TTS"])
async def synthesize_speech(request: SynthesisRequest, background_tasks: BackgroundTasks):
    """
    Türkçe metni sese dönüştür.

    - **text**: Sentezlenecek metin (1-5000 karakter)
    - **voice**: Kullanılacak ses (varsayılan: default)
    - **speed**: Konuşma hızı 0.5-2.0 (varsayılan: 1.0)
    - **pitch**: Perde çarpanı 0.5-2.0 (varsayılan: 1.0)
    - **format**: Çıktı formatı (wav, mp3, ogg)
    """
    try:
        engine = get_engine()

        # Generate unique ID
        audio_id = str(uuid.uuid4())[:8]

        # Estimate duration
        estimated_duration = len(request.text) / 5.0 / request.speed  # rough estimate

        # Synthesize in background
        def synthesize():
            audio = engine.synthesize(
                text=request.text,
                voice=request.voice,
                speed=request.speed,
                pitch=request.pitch,
            )

            # Save to temp file
            temp_dir = Path(tempfile.gettempdir()) / "turkishvoice"
            temp_dir.mkdir(exist_ok=True)
            temp_file = temp_dir / f"{audio_id}.wav"

            engine.save(audio, str(temp_file))
            _audio_storage[audio_id] = str(temp_file)

        background_tasks.add_task(synthesize)

        return SynthesisResponse(
            audio_id=audio_id,
            status="processing",
            duration_seconds=estimated_duration,
            message="Metin sentezleniyor. Sonucu /api/v1/synthesize/{audio_id} endpointinden alın.",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/synthesize/{audio_id}", tags=["TTS"])
async def get_synthesis_result(audio_id: str):
    """
    Sentez sonucunu al.

    Tamamlanan sentez işleminin ses dosyasını döndürür.
    """
    if audio_id not in _audio_storage:
        raise HTTPException(status_code=404, detail="Ses bulunamadı veya hala işleniyor")

    file_path = Path(_audio_storage[audio_id])

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Ses dosyası silinmiş")

    return FileResponse(
        path=str(file_path),
        media_type="audio/wav",
        filename=f"turkishvoice_{audio_id}.wav",
    )


@app.post("/api/v1/synthesize/stream", tags=["TTS"])
async def synthesize_stream(request: SynthesisRequest):
    """
    Sentez sonucunu stream olarak al.

    Ses dosyası oluşturulurken stream olarak döndürülür.
    Uzun metinler için önerilir.
    """
    try:
        engine = get_engine()

        # Synthesize
        audio = engine.synthesize(
            text=request.text,
            voice=request.voice,
            speed=request.speed,
            pitch=request.pitch,
        )

        # Save to temp file for streaming
        temp_dir = Path(tempfile.gettempdir()) / "turkishvoice"
        temp_dir.mkdir(exist_ok=True)
        temp_file = temp_dir / f"stream_{uuid.uuid4().hex[:8]}.wav"

        engine.save(audio, str(temp_file))

        # Delete after streaming
        def cleanup():
            if temp_file.exists():
                temp_file.unlink()

        return StreamingResponse(
            iter([open(temp_file, 'rb').read()]),
            media_type="audio/wav",
            headers={
                "Content-Disposition": f"attachment; filename=turkishvoice_stream.wav",
                "X-Content-Type-Options": "nosniff",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/voices", response_model=VoicesListResponse, tags=["Voices"])
async def list_voices():
    """
    Mevcut sesleri listele.

    Kullanılabilir Türkçe seslerin listesini döndürür.
    """
    engine = get_engine()
    voices = engine.get_available_voices()

    return VoicesListResponse(
        voices=[VoiceInfo(**v) for v in voices],
        count=len(voices),
    )


@app.post("/api/v1/voices/clone", response_model=CloneResponse, tags=["Voices"])
async def clone_voice(
    voice_name: str,
    description: Optional[str] = None,
    language: Literal["tr", "mixed"] = "tr",
):
    """
    Ses klonla.

    Not: Bu endpoint şu anda geliştirme aşamasındadır.
    Gerçek ses klonlama için referans ses dosyası gereklidir.

    - **voice_name**: Klonlanan sese verilecek isim
    - **description**: İsteğe bağlı açıklama
    - **language**: Sesin dili (tr veya mixed)
    """
    # Placeholder implementation
    voice_id = f"cloned_{uuid.uuid4().hex[:8]}"

    return CloneResponse(
        voice_id=voice_id,
        status="coming_soon",
        message="Ses klonlama özelliği yakında eklenecek. "
                "Şu an için varsayılan seslerimizi kullanabilirsiniz.",
    )


@app.post("/api/v1/batch", response_model=BatchSynthesisResponse, tags=["Batch"])
async def create_batch(request: BatchSynthesisRequest, background_tasks: BackgroundTasks):
    """
    Toplu sentez işlemi oluştur.

    Birden fazla metni toplu olarak sentezler.

    - **items**: Sentezlenecek metin listesi (max 1000)
    - **callback_url**: Tamamlandığında bildirim gönderilecek URL (isteğe bağlı)
    """
    batch_id = f"batch_{uuid.uuid4().hex[:8]}"

    def process_batch():
        engine = get_engine()
        for i, item in enumerate(request.items):
            try:
                audio = engine.synthesize(
                    text=item.text,
                    voice=item.voice,
                    speed=item.speed,
                    pitch=item.pitch,
                )
                # Save result
                # In production, save to cloud storage or similar
            except Exception as e:
                print(f"Batch item {i} failed: {e}")

    background_tasks.add_task(process_batch)

    return BatchSynthesisResponse(
        batch_id=batch_id,
        status="queued",
        total_items=len(request.items),
    )


@app.get("/api/v1/info", tags=["Info"])
async def get_info():
    """
    Motor bilgilerini al.

    TurkishVoice motorunun detaylı bilgilerini döndürür.
    """
    engine = get_engine()
    info = engine.get_engine_info()

    return {
        "name": info["name"],
        "version": info["version"],
        "sample_rate": info["sample_rate"],
        "model_type": info["model_type"],
        "vocoder_type": info["vocoder_type"],
        "features": [
            "text_normalization",
            "grapheme_to_phoneme",
            "vowel_harmony",
            "stress_marking",
            "voice_synthesis",
        ],
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": True,
        "status_code": exc.status_code,
        "detail": exc.detail,
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "error": True,
        "status_code": 500,
        "detail": str(exc),
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize engine on startup."""
    get_engine()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
