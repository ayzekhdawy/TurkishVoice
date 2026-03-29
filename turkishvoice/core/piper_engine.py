"""
Piper TTS Engine Integration

Real-time Turkish text-to-speech using Piper TTS.
"""

import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Any
import wave
import io
import logging

logger = logging.getLogger(__name__)


class PiperTTSVoice:
    """
    Piper TTS engine for Turkish speech synthesis.

    Piper is a fast, local neural TTS system that runs on CPU.
    Turkish voices available: dfki, fahrettin, fettah
    """

    # Available Turkish voices
    TURKISH_VOICES: Dict[str, str] = {
        'dfki': 'tr_TR-dfki-medium.onnx',
        'fahrettin': 'tr_TR-fahrettin-medium.onnx',
        'fettah': 'tr_TR-fettah-medium.onnx',
    }

    def __init__(
        self,
        voice: str = 'dfki',
        model_path: Optional[Path] = None,
        config_path: Optional[Path] = None,
        use_gpu: bool = False,
        sample_rate: int = 16000,
    ):
        """
        Initialize Piper TTS engine.

        Args:
            voice: Voice identifier ('dfki', 'fahrettin', 'fettah')
            model_path: Path to .onnx model file
            config_path: Path to .onnx.json config file
            use_gpu: Use GPU acceleration (requires onnxruntime-gpu)
            sample_rate: Audio sample rate (default 16000 for Piper)
        """
        self.voice_name = voice
        self.model_path = model_path
        self.config_path = config_path
        self.use_gpu = use_gpu
        self.sample_rate = sample_rate

        self._voice = None
        self._is_loaded = False

    @property
    def is_loaded(self) -> bool:
        """Check if the model is loaded."""
        return self._is_loaded

    def load(self):
        """Load the Piper model."""
        if self._is_loaded:
            return

        try:
            from piper import PiperVoice

            # Determine model path
            if self.model_path is None:
                from turkishvoice.utils.model_downloader import get_voice_path
                self.model_path = get_voice_path(self.voice_name)

            if self.model_path is None or not Path(self.model_path).exists():
                raise FileNotFoundError(
                    f"Model not found for voice '{self.voice_name}'. "
                    f"Run 'turkishvoice download {self.voice_name}' first."
                )

            # Load the model
            logger.info(f"Loading Piper voice: {self.model_path}")
            self._voice = PiperVoice.load(str(self.model_path))
            self._is_loaded = True
            logger.info("Piper voice loaded successfully")

        except ImportError as e:
            raise ImportError(
                "Piper TTS is not installed. Run: pip install piper-tts"
            ) from e
        except Exception as e:
            logger.error(f"Failed to load Piper voice: {e}")
            raise

    def _ensure_loaded(self):
        """Ensure model is loaded before synthesis."""
        if not self._is_loaded:
            self.load()

    def synthesize(
        self,
        text: str,
        speed: float = 1.0,
        pitch: float = 1.0,
    ) -> np.ndarray:
        """
        Synthesize speech from text.

        Args:
            text: Turkish text to synthesize
            speed: Speech rate (0.5-2.0, default 1.0)
            pitch: Pitch multiplier (not directly supported by Piper)

        Returns:
            Audio waveform as numpy array (float32, mono)
        """
        self._ensure_loaded()

        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Piper doesn't support speed/pitch directly
        # We'll apply post-processing for speed adjustment
        audio = self._synthesize_internal(text)

        # Apply speed modification if needed
        if speed != 1.0:
            audio = self._apply_speed_change(audio, speed)

        return audio.astype(np.float32)

    def _synthesize_internal(self, text: str) -> np.ndarray:
        """Internal synthesis using Piper."""
        import tempfile

        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Synthesize to file
            with wave.open(tmp_path, 'wb') as wav_file:
                self._voice.synthesize_wav(text, wav_file)

            # Read the WAV file
            with wave.open(tmp_path, 'rb') as wav_file:
                n_channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                n_frames = wav_file.getnframes()

                # Read audio data
                audio_data = wav_file.readframes(n_frames)

                # Convert to numpy array
                if sample_width == 2:
                    audio = np.frombuffer(audio_data, dtype=np.int16)
                elif sample_width == 4:
                    audio = np.frombuffer(audio_data, dtype=np.int32)
                else:
                    audio = np.frombuffer(audio_data, dtype=np.uint8)

                # Normalize to float32 [-1, 1]
                audio = audio.astype(np.float32) / (32768.0 if sample_width == 2 else 128.0)

                return audio

        finally:
            # Clean up temp file
            try:
                Path(tmp_path).unlink()
            except:
                pass

    def synthesize_streaming(self, text: str):
        """
        Synthesize speech with streaming output.

        Yields audio chunks as they're generated.
        """
        self._ensure_loaded()

        # Piper supports streaming synthesis
        for audio_chunk in self._voice.synthesize(text):
            # Convert bytes to numpy
            audio = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
            yield audio

    def _apply_speed_change(self, audio: np.ndarray, speed: float) -> np.ndarray:
        """Apply speed change using resampling."""
        if speed == 1.0:
            return audio

        # Resample to change speed
        new_length = int(len(audio) / speed)
        indices = np.linspace(0, len(audio) - 1, new_length)
        return np.interp(indices, np.arange(len(audio)), audio)

    def get_voice_info(self) -> Dict[str, Any]:
        """Get information about the current voice."""
        from turkishvoice.utils.model_downloader import TURKISH_VOICES

        info = TURKISH_VOICES.get(self.voice_name, {})
        return {
            'name': self.voice_name,
            'model': self.TURKISH_VOICES.get(self.voice_name, 'unknown'),
            'quality': info.get('quality', 'unknown'),
            'size': info.get('size', 'unknown'),
            'sample_rate': self.sample_rate,
            'is_loaded': self._is_loaded,
        }

    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get list of available Turkish voices."""
        from turkishvoice.utils.model_downloader import TURKISH_VOICES

        voices = []
        for name, model in self.TURKISH_VOICES.items():
            voices.append({
                'id': name,
                'name': name.capitalize(),
                'gender': 'neutral',
                'age': 'adult',
                'description': f"Turkish {name} voice (Piper TTS)",
            })
        return voices


class EdgeTTSVoice:
    """
    Microsoft Edge TTS (online) for high-quality Turkish synthesis.

    Requires internet connection.
    """

    TURKISH_VOICES = {
        'emel': 'tr-TR-EmelNeural',
        'ahmet': 'tr-TR-AhmetNeural',
    }

    def __init__(self, voice: str = 'emel'):
        """
        Initialize Edge TTS.

        Args:
            voice: Voice identifier ('emel' or 'ahmet')
        """
        self.voice_name = voice
        self._is_loaded = True  # No model to load

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def load(self):
        """No-op for Edge TTS."""
        pass

    async def synthesize_async(
        self,
        text: str,
        speed: float = 1.0,
        pitch: float = 1.0,
    ) -> np.ndarray:
        """
        Synthesize speech using Edge TTS (async).

        Args:
            text: Turkish text to synthesize
            speed: Speech rate (0.5-2.0)
            pitch: Pitch shift (-50 to 50 semitones)

        Returns:
            Audio waveform as numpy array
        """
        import edge_tts
        import tempfile
        from pathlib import Path

        # Get Edge voice ID
        voice_id = self.TURKISH_VOICES.get(self.voice_name, 'tr-TR-EmelNeural')

        # Create communicate object
        communicate = edge_tts.Communicate(text, voice_id)

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            await communicate.save(tmp_path)

            # Read the MP3 file
            audio = self._read_audio_file(tmp_path)

            # Apply speed/pitch if needed
            if speed != 1.0:
                audio = self._apply_speed_change(audio, speed)

            return audio

        finally:
            # Clean up
            try:
                Path(tmp_path).unlink()
            except:
                pass

    def synthesize(
        self,
        text: str,
        speed: float = 1.0,
        pitch: float = 1.0,
    ) -> np.ndarray:
        """Synchronous wrapper for synthesize_async."""
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(
            self.synthesize_async(text, speed, pitch)
        )

    def _read_audio_file(self, path: str) -> np.ndarray:
        """Read audio file (MP3/WAV) to numpy array."""
        try:
            # Try soundfile first (supports MP3)
            import soundfile as sf
            audio, sr = sf.read(path)
            return audio.astype(np.float32)
        except ImportError:
            # Fallback: use pydub
            from pydub import AudioSegment
            sound = AudioSegment.from_file(path)
            sound = sound.set_channels(1).set_frame_rate(16000)
            return np.array(sound.get_array_of_samples(), dtype=np.float32) / 32768.0
        except Exception as e:
            logger.error(f"Failed to read audio: {e}")
            raise

    def _apply_speed_change(self, audio: np.ndarray, speed: float) -> np.ndarray:
        """Apply speed change using resampling."""
        if speed == 1.0:
            return audio

        new_length = int(len(audio) / speed)
        indices = np.linspace(0, len(audio) - 1, new_length)
        return np.interp(indices, np.arange(len(audio)), audio)

    def get_voice_info(self) -> Dict[str, Any]:
        """Get voice information."""
        return {
            'name': self.voice_name,
            'model': 'Edge TTS (Microsoft Azure)',
            'quality': 'neural',
            'sample_rate': 24000,
            'is_loaded': True,
            'requires_internet': True,
        }

    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get available Edge TTS voices."""
        return [
            {
                'id': 'emel',
                'name': 'Emel (Neural)',
                'gender': 'female',
                'age': 'adult',
                'description': 'Turkish female neural voice (Microsoft Edge)',
            },
            {
                'id': 'ahmet',
                'name': 'Ahmet (Neural)',
                'gender': 'male',
                'age': 'adult',
                'description': 'Turkish male neural voice (Microsoft Edge)',
            },
        ]
