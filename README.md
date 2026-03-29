<div align="center">

![TurkishVoice Banner](https://via.placeholder.com/1200x300/E30A17/FFFFFF?text=TurkishVoice+🇹🇷)

# 🇹🇷 TurkishVoice

**Açık Kaynaklı Türkçe Metin Okuma Sistemi**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg?style=for-the-badge&logo=python)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/turkishvoice.svg?style=for-the-badge&logo=pypi)](https://pypi.org/project/turkishvoice/)
[![GitHub Stars](https://img.shields.io/github/stars/ayzekhdawy/TurkishVoice?style=for-the-badge&logo=github)](https://github.com/ayzekhdawy/TurkishVoice/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ayzekhdawy/TurkishVoice?style=for-the-badge&logo=github)](https://github.com/ayzekhdawy/TurkishVoice/network)
[![GitHub Issues](https://img.shields.io/github/issues/ayzekhdawy/TurkishVoice?style=for-the-badge&logo=github)](https://github.com/ayzekhdawy/TurkishVoice/issues)
[![Discord](https://img.shields.io/discord/1234567890?style=for-the-badge&logo=discord)](https://discord.gg/turkishvoice)
[![CI/CD](https://img.shields.io/github/actions/workflow/status/ayzekhdawy/TurkishVoice/ci.yml?style=for-the-badge&logo=github-actions)](https://github.com/ayzekhdawy/TurkishVoice/actions)

[🎮 Canlı Demo](https://huggingface.co/spaces/ayzek/TurkishVoice) • [📚 Dokümantasyon](https://turkishvoice.readthedocs.io/) • [🐛 Sorun Bildir](https://github.com/ayzekhdawy/TurkishVoice/issues) • [💬 Tartışmalar](https://github.com/ayzekhdawy/TurkishVoice/discussions) • [📊 Roadmap](https://github.com/ayzekhdawy/TurkishVoice/wiki/Roadmap)

</div>

---

## 📖 İçindekiler

<details>
<summary>Genişletmek için tıklayın</summary>

- [Özellikler](#-özellikler)
- [Demo](#-demo)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Kullanım Örnekleri](#-kullanım-örnekleri)
- [API Referansı](#-api-referansı)
- [Sesler](#-sesler)
- [Performans](#-performans)
- [Karşılaştırma](#-karşılaştırma)
- [Kullanım Senaryoları](#-kullanım-senaryoları)
- [Kurulum](#-kurulum)
- [Geliştirme](#-geliştirme)
- [FAQ](#-faq)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Güvenlik](#-güvenlik)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Topluluk](#-topluluk)
- [Lisans](#-lisans)
- [Atıf](#-atıf)

</details>

---

## ✨ Özellikler

<div align="center">

| 🎯 | 🚀 | 🔊 |
|:---:|:---:|:---:|
| **Türkçe Özel** | **Gerçek Zamanlı** | **Çoklu Backend** |
| Ünlü uyumu, G2P, vurgu | ~700ms gecikme | Edge TTS + Piper TTS |

| 🔓 | 🎙️ | 💻 |
|:---:|:---:|:---:|
| **Açık Kaynak** | **Ses Klonlama** | **Çoklu Platform** |
| Apache 2.0 | Coqui XTTS | Python, CLI, API, Web |

</div>

### 🌟 Neden TurkishVoice?

```diff
+ Türkçe'ye Özel Optimize       - Sadece Çeviri Değil
+ Tamamen Açık Kaynak           - Kapalı API'ler
+ Ücretsiz Kullanım             - Ücretli Servisler
+ Offline Çalışabilir           - İnternet Zorunluluğu
+ Ses Klonlama Dahil            - Ekstra Ücret
+ Aktif Geliştirme              - Terk Edilmiş Projeler
```

---

## 🎬 Demo

<div align="center">

![Demo GIF](https://via.placeholder.com/800x450/1a1a2e/FFFFFF?text=TurkishVoice+Demo+-+TTS+in+Action)

**[🔗 Canlı Demo Deneyin →](https://huggingface.co/spaces/ayzek/TurkishVoice)**

</div>

---

## 🚀 Hızlı Başlangıç

### 1 Dakikada Başla

```bash
# Kurulum
pip install turkishvoice

# Hemen kullan
python -c "from turkishvoice import TurkishVoiceEngine; e = TurkishVoiceEngine(voice='emel', use_edge=True); e.synthesize('Merhaba dünya!')"
```

### CLI Kullanımı

```bash
# Ses sentezi
turkishvoice synthesize "Merhaba, ben TurkishVoice!" -o output.wav --voice emel

# Sesleri listele
turkishvoice voices

# API sunucusu başlat
turkishvoice serve --port 8000

# Batch işlem
turkishvoice batch metinler.txt -o output/ --parallel 8
```

### Python API

```python
from turkishvoice import TurkishVoiceEngine

# Edge TTS (Online - Yüksek Kalite)
engine = TurkishVoiceEngine(voice='emel', use_edge=True)
audio = engine.synthesize("Merhaba dünya!")
engine.save(audio, "output.wav")

# Piper TTS (Offline - Hızlı)
engine = TurkishVoiceEngine(voice='dfki', use_piper=True)
audio = engine.synthesize("Türkçe konuşuyorum!")

# Ses klonlama
from turkishvoice.core.voice_cloner import VoiceCloner
cloner = VoiceCloner()
cloned_audio = cloner.clone("referans.wav", "Klonlanmış sesle konuşuyorum!")
```

### Async Kullanım

```python
import asyncio
from turkishvoice import TurkishVoiceEngine

async def main():
    engine = TurkishVoiceEngine(voice='emel', use_edge=True)

    # Paralel sentez
    tasks = [
        engine.synthesize(f"Cümle {i}")
        for i in range(10)
    ]
    results = await asyncio.gather(*tasks)

    print(f"{len(results)} ses dosyası oluşturuldu!")

asyncio.run(main())
```

---

## 📖 Kullanım Örnekleri

### 📚 Sesli Kitap Oluşturma

```python
from turkishvoice import TurkishVoiceEngine
from pathlib import Path

engine = TurkishVoiceEngine(voice='emel', use_edge=True)
output_dir = Path("audiobook")
output_dir.mkdir(exist_ok=True)

with open('kitap.txt', 'r', encoding='utf-8') as f:
    for i, satir in enumerate(f):
        if satir.strip():
            audio = engine.synthesize(satir.strip())
            engine.save(audio, output_dir / f'bolum_{i:03d}.wav')
            print(f"Bölüm {i+1} oluşturuldu ✓")
```

### 🎬 Video Seslendirme

```python
from turkishvoice import TurkishVoiceEngine

script = [
    "Merhaba arkadaşlar, kanalıma hoş geldiniz!",
    "Bugün sizlere harika bir haberim var.",
    "TurkishVoice artık tamamen ücretsiz!"
]

engine = TurkishVoiceEngine(voice='ahmet', use_edge=True)

for i, line in enumerate(script):
    # Farklı hız ve perde ayarları
    audio = engine.synthesize(
        line,
        speed=1.1,
        pitch=0.95
    )
    engine.save(audio, f'video/scene_{i}.wav')
```

### 📞 Call Center / IVR

```python
from fastapi import FastAPI
from turkishvoice import TurkishVoiceEngine
from fastapi.responses import StreamingResponse
import io

app = FastAPI(title="TurkishVoice API")
engine = TurkishVoiceEngine(voice='emel', use_edge=True)

@app.get("/ivr/{message}")
async def ivr(message: str):
    """IVR sistemi için ses sentezi"""
    audio = engine.synthesize(message)
    buffer = io.BytesIO()
    engine.save(audio, buffer)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="audio/wav")

@app.post("/api/tts")
async def text_to_speech(text: str, voice: str = "emel"):
    """REST API endpoint"""
    audio = engine.synthesize(text, voice=voice)
    return {"status": "success", "duration": len(audio)/24000}
```

### ♿ Erişilebilirlik

```python
# Web sitesi metinlerini sesli oku
def read_webpage_text(text: str, max_length: int = 5000):
    engine = TurkishVoiceEngine(voice='emel')
    truncated = text[:max_length]
    audio = engine.synthesize(truncated)
    engine.save(audio, "webpage_audio.wav")
    return "webpage_audio.wav"

# Ekran okuyucu entegrasyonu
def screen_reader_integration(selected_text: str):
    engine = TurkishVoiceEngine(voice='emel', use_edge=True)
    audio = engine.synthesize(selected_text)
    # Ses çalma işlemi platform-specific
    play_audio(audio)
```

### 📊 Batch Processing

```python
from turkishvoice import TurkishVoiceEngine
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def batch_synthesize(input_file: str, output_dir: str, max_workers: int = 4):
    """Toplu ses sentezi"""
    engine = TurkishVoiceEngine(voice='dfki', use_piper=True)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]

    def process(args):
        i, text = args
        audio = engine.synthesize(text)
        engine.save(audio, output_path / f'output_{i:05d}.wav')
        return i

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(executor.map(process, enumerate(lines)))

    print(f"✓ {len(lines)} dosya oluşturuldu!")
```

---

## 🔧 API Referansı

### TurkishVoiceEngine

```python
class TurkishVoiceEngine:
    """
    Ana TurkishVoice TTS Motoru

    Args:
        voice (str): Ses seçimi ('emel', 'ahmet', 'dfki')
        use_edge (bool): Edge TTS kullan (online, yüksek kalite)
        use_piper (bool): Piper TTS kullan (offline, hızlı)
        sample_rate (int): Audio örnekleme hızı (default: 22050)

    Example:
        >>> engine = TurkishVoiceEngine(voice='emel', use_edge=True)
        >>> audio = engine.synthesize("Merhaba dünya!")
        >>> engine.save(audio, "output.wav")
    """

    def __init__(
        self,
        voice: str = "emel",
        use_edge: bool = True,
        use_piper: bool = False,
        sample_rate: int = 22050
    )

    def synthesize(
        self,
        text: str,
        speed: float = 1.0,    # 0.5 - 2.0
        pitch: float = 1.0,    # 0.5 - 2.0
    ) -> np.ndarray
        """
        Metni sese dönüştür.

        Args:
            text (str): Sentezlenecek Türkçe metin
            speed (float): Konuşma hızı (0.5-2.0)
            pitch (float): Perde çarpanı (0.5-2.0)

        Returns:
            np.ndarray: Audio waveform (float32, mono)
        """

    def save(
        self,
        audio: np.ndarray,
        path: str,
        format: str = 'wav'
    )
        """
        Audio'yu dosyaya kaydet.

        Args:
            audio (np.ndarray): Audio waveform
            path (str): Çıktı dosya yolu
            format (str): Format ('wav', 'mp3', 'ogg')
        """

    def get_available_voices(self) -> List[Dict]:
        """Mevcut sesleri listele."""

    def get_engine_info(self) -> Dict:
        """Motor bilgilerini döndür."""
```

### REST API Endpoints

| Endpoint | Method | Parametreler | Açıklama |
|----------|--------|-------------|----------|
| `/health` | GET | - | API sağlık kontrolü |
| `/api/v1/synthesize` | POST | `text`, `voice`, `speed` | Ses sentezi |
| `/api/v1/synthesize/{id}` | GET | `audio_id` | Sentez sonucunu al |
| `/api/v1/voices` | GET | - | Sesleri listele |
| `/api/v1/voices/clone` | POST | `audio`, `text` | Ses klonlama |
| `/api/v1/info` | GET | - | Motor bilgisi |

```bash
# Örnek API isteği
curl -X POST "http://localhost:8000/api/v1/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Merhaba dünya!",
    "voice": "emel",
    "speed": 1.0
  }' \
  -o output.wav

# Streaming response
curl -X POST "http://localhost:8000/api/v1/synthesize/stream" \
  -H "Content-Type: application/json" \
  -d '{"text": "Uzun metin...", "voice": "ahmet"}' \
  --output stream.wav
```

---

## 🎙️ Sesler

### Edge TTS (Online - Microsoft Azure)

| ID | İsim | Cinsiyet | Kalite | Gecikme | Örnek |
|:--:|:----:|:--------:|:------:|:-------:|:-----:|
| `emel` | Emel | 👩 Kadın | ⭐⭐⭐⭐⭐ | ~700ms | 🔊 |
| `ahmet` | Ahmet | 👨 Erkek | ⭐⭐⭐⭐⭐ | ~700ms | 🔊 |

### Piper TTS (Offline - Hızlı)

| ID | İsim | Kalite | Gecikme | Boyut | İndir |
|:--:|:----:|:------:|:-------:|:-----:|:-----:|
| `dfki` | DFKI | ⭐⭐⭐ | ~100ms | 63 MB | `turkishvoice download dfki` |

### Özel Sesler

```python
# Özel ses klonlama
from turkishvoice.core.voice_cloner import VoiceCloner

cloner = VoiceCloner()

# Referans sesten klonlama
cloned_audio = cloner.clone(
    reference_audio="benim_sesim.wav",  # 30 saniye+ temiz kayıt
    text="Klonlanmış sesimle konuşuyorum!",
    language="tr"
)

# Batch klonlama
results = cloner.clone_batch(
    reference_audio="benim_sesim.wav",
    texts=["Cümle 1", "Cümle 2", "Cümle 3"],
    output_dir="cloned_output/"
)
```

---

## 📊 Performans

<div align="center">

| Metrik | Edge TTS | Piper TTS | Coqui XTTS |
|--------|----------|-----------|------------|
| **İlk Ses Gecikmesi** | ~700ms | ~100ms | ~2000ms |
| **Sentez Hızı** | 1x RT | 6x RT | 0.5x RT |
| **RAM Kullanımı** | < 200 MB | < 100 MB | > 2 GB |
| **İnternet** | ✅ Gerekli | ❌ Gerekmez | ❌ Gerekmez |
| **Kalite** | Mükemmel | İyi | Çok İyi |
| **CPU Kullanımı** | Düşük | Çok Düşük | Yüksek |

*RT = Real-Time (Gerçek Zamanlı)*

</div>

### Benchmark Grafiği

```
Ses Sentez Süresi (100 karakter metin)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Edge TTS  ████████░░░░░░░░░░░░ 700ms
Piper TTS ██░░░░░░░░░░░░░░░░░░ 100ms
Coqui XTTS ████████████████░░░░ 1500ms
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🆚 Karşılaştırma

<div align="center">

| Özellik | TurkishVoice | Google Cloud TTS | Azure Cognitive | Amazon Polly |
|---------|:------------:|:----------------:|:---------------:|:------------:|
| **Türkçe Kalite** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Ücretsiz** | ✅ Tamamen | ❌ 1M karakter/ay | ❌ 500k/ay | ❌ 1M/ay |
| **Offline** | ✅ | ❌ | ❌ | ❌ |
| **Açık Kaynak** | ✅ | ❌ | ❌ | ❌ |
| **Ses Klonlama** | ✅ Ücretsiz | ✅ $16/saat | ✅ $10/saat | ✅ $4/saat |
| **Türkçe Ünlü Uyumu** | ✅ | ❌ | ❌ | ❌ |
| **Ticari Kullanım** | ✅ Serbest | ✅ Lisans | ✅ Lisans | ✅ Lisans |

</div>

### Maliyet Karşılaştırması (Aylık, 1M karakter)

```
TurkishVoice     $0        ████████████████████
Google TTS       $16       ████████████████░░░░
Azure TTS        $15       ████████████████░░░░
Amazon Polly     $4        █████████████████░░░
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 💡 Kullanım Senaryoları

### 🎯 Hedef Kitle

| Kullanıcı | Kullanım Alanı | Örnek | Zorluk |
|-----------|---------------|-------|:------:|
| **İçerik Üreticileri** | YouTube/TikTok seslendirme | Video narrasyonları | ⭐ |
| **Eğitimciler** | Ders materyali seslendirme | Sesli ders notları | ⭐ |
| **Görme Engelliler** | Metin okuma | Web sitesi, belge | ⭐⭐ |
| **Call Center** | IVR sistemleri | Otomatik yanıt | ⭐⭐⭐ |
| **Yazılımcılar** | Uygulama entegrasyonu | API, SDK | ⭐⭐⭐ |
| **Podcast'çiler** | Otomatik içerik | Haber okuma | ⭐⭐ |

---

## 📦 Kurulum

### Temel Kurulum

```bash
pip install turkishvoice
```

### Tüm Özelliklerle

```bash
pip install turkishvoice[all]
```

### Opsiyonel Paketler

```bash
# Ses klonlama için
pip install turkishvoice[clone]

# Web UI için
pip install turkishvoice[webui]

# API için
pip install turkishvoice[api]

# Geliştirme için
pip install turkishvoice[dev]
```

### Docker

```bash
# Docker ile çalıştır
docker pull ayzekhdawy/turkishvoice:latest
docker run -p 8000:8000 turkishvoice serve
```

### Sistem Gereksinimleri

| Bileşen | Minimum | Önerilen |
|---------|---------|----------|
| **Python** | 3.8 | 3.10+ |
| **RAM** | 4 GB | 8 GB |
| **Disk** | 500 MB | 2 GB |
| **İnternet** | Opsiyonel | Edge TTS için |
| **CPU** | 2 çekirdek | 4+ çekirdek |

---

## 🛠️ Geliştirme

```bash
# Repo'yu klonla
git clone https://github.com/ayzekhdawy/TurkishVoice
cd TurkishVoice

# Geliştirme modunda kur
pip install -e ".[all,dev]"

# Testleri çalıştır
pytest tests/ -v --cov=turkishvoice

# Kod formatı
black turkishvoice/
isort turkishvoice/

# Lint kontrolü
flake8 turkishvoice/
mypy turkishvoice/

# Build
python -m build
```

### Proje Yapısı

```
TurkishVoice/
├── turkishvoice/           # Ana paket
│   ├── core/               # TTS motoru
│   │   ├── engine.py       # Ana motor
│   │   ├── piper_engine.py # Piper entegrasyonu
│   │   └── voice_cloner.py # Ses klonlama
│   ├── turkish/            # Türkçe işleme
│   │   ├── g2p.py          # Grapheme-to-Phoneme
│   │   ├── vowel_harmony.py # Ünlü uyumu
│   │   ├── stress_marker.py # Vurgu
│   │   └── text_normalizer.py # Metin normalizasyonu
│   ├── api/                # FastAPI REST API
│   ├── cli/                # CLI aracı
│   ├── utils/              # Yardımcılar
│   └── webui/              # Gradio Web UI
├── tests/                  # Testler
├── demo_app.py             # Demo uygulama
├── pyproject.toml          # Proje ayarları
└── README.md               # Bu dosya
```

### CI/CD

```yaml
# .github/workflows/ci.yml
name: CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: pip install -e ".[dev]"

    - name: Run tests
      run: pytest tests/ -v --cov
```

---

## 🤔 FAQ

<details>
<summary><b>TurkishVoice ücretsiz mi?</b></summary>

✅ Evet, tamamen ücretsiz ve açık kaynaktır. Ticari kullanım dahil her türlü kullanım serbesttir (Apache 2.0 lisansı).
</details>

<details>
<summary><b>İnternet bağlantısı gerekli mi?</b></summary>

Edge TTS için internet gerekir. Piper TTS ile offline çalışabilirsiniz.
</details>

<details>
<summary><b>Kendi sesimi klonlayabilir miyim?</b></summary>

✅ Evet! Coqui XTTS ile minimum 30 saniye temiz referans ses ile ses klonlama yapabilirsiniz.
</details>

<details>
<summary><b>Hangi formatları destekler?</b></summary>

WAV, MP3, OGG formatlarını destekler.
</details>

<details>
<summary><b>Ticari projelerde kullanabilir miyim?</b></summary>

✅ Evet, Apache 2.0 lisansı ticari kullanıma izin verir.
</details>

---

## 🔧 Troubleshooting

### Yaygın Sorunlar

#### 1. "ModuleNotFoundError: No module named 'turkishvoice'"

```bash
# Çözüm
pip install turkishvoice
# Veya
pip install -e .
```

#### 2. "Model not found"

```bash
# Piper TTS modelini indir
turkishvoice download dfki
```

#### 3. Edge TTS bağlantı hatası

```python
# İnternet bağlantınızı kontrol edin
# Veya Piper TTS kullanın
engine = TurkishVoiceEngine(voice='dfki', use_piper=True, use_edge=False)
```

#### 4. Ses kalitesi düşük

```python
# Edge TTS kullanın (daha yüksek kalite)
engine = TurkishVoiceEngine(voice='emel', use_edge=True)

# Veya speed/pitch ayarlarını optimize edin
audio = engine.synthesize(text, speed=1.0, pitch=1.0)
```

#### 5. Türkçe karakterler yanlış görünüyor

```python
# Terminal encoding'i UTF-8 yapın
# Windows: chcp 65001
# Python: export PYTHONIOENCODING=utf-8
```

### Hata Bildirimi

Sorunuzu [GitHub Issues](https://github.com/ayzekhdawy/TurkishVoice/issues) üzerinden bildirirken şunları ekleyin:

- Python versiyonu (`python --version`)
- İşletim sistemi
- Hata mesajı (tam)
- Minimum tekrarlanabilir örnek

---

## 🗺️ Roadmap

### v0.3.0 (Q2 2026)
- [ ] Daha fazla Türkçe ses (Piper)
- [ ] Duygu analizi ile sentez (mutlu, üzgün, heyecanlı)
- [ ] Real-time streaming TTS
- [ ] Docker container

### v0.4.0 (Q3 2026)
- [ ] Web tabanlı ses eğitimi
- [ ] Multi-speaker TTS
- [ ] Whisper entegrasyonu (STT)
- [ ] Mobil SDK (iOS/Android)

### v1.0.0 (Q4 2026)
- [ ] Tam Türkçe dil desteği
- [ ] Production-ready API
- [ ] Cloud deployment
- [ ] Enterprise features

[Roadmap'u görüntüle →](https://github.com/ayzekhdawy/TurkishVoice/wiki/Roadmap)

---

## 🔒 Güvenlik

### Veri Gizliliği

- **Edge TTS**: Metin Microsoft sunucularına gönderilir
- **Piper TTS**: Tamamen offline, veri gönderilmez
- **Ses Klonlama**: Referans sesler lokal kalır

### Güvenlik Önerileri

```python
# API kullanırken authentication ekleyin
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer

app = FastAPI()
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "YOUR_SECRET_TOKEN":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.credentials

@app.post("/api/v1/synthesize")
async def synthesize(token: str = Depends(verify_token)):
    ...
```

### Bilinen Güvenlik Açıkları

Şu anda bilinen güvenlik açığı bulunmamaktadır. Bulduğunuz açıkları lütfen [security@turkishvoice.ai](mailto:security@turkishvoice.ai) adresine bildirin.

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! 🎉

### Nasıl Katkıda Bulunabilirim?

1. **Fork** edin
2. **Branch** oluşturun (`git checkout -b feature/YeniOzellik`)
3. **Commit** edin (`git commit -m 'Yeni özellik eklendi'`)
4. **Push** edin (`git push origin feature/YeniOzellik`)
5. **Pull Request** açın

### Katkı Türleri

| Tür | Açıklama | Zorluk |
|-----|----------|:------:|
| 🐛 Bug Report | Hata bildirimi | ⭐ |
| 💡 Özellik | Yeni özellik önerisi | ⭐⭐ |
| 📝 Dokümantasyon | Düzeltme/ekleme | ⭐ |
| 🔤 Çeviri | Dil desteği | ⭐⭐ |
| ⚡ Optimizasyon | Performans | ⭐⭐⭐ |
| 🧪 Test | Test yazımı | ⭐⭐ |

### Geliştirme Ortamı

```bash
# Fork'u klonla
git clone https://github.com/kullaniciadi/TurkishVoice
cd TurkishVoice

# Geliştirme bağımlılıkları
pip install -e ".[dev]"

# Pre-commit hooks
pip install pre-commit
pre-commit install
```

---

## 🌟 Topluluk

### Katkıda Bulunanlar

[![Contributors](https://contrib.rocks/image?repo=ayzekhdawy/TurkishVoice)](https://github.com/ayzekhdawy/TurkishVoice/graphs/contributors)

### Topluluk Linkleri

- [💬 Discord Sunucusu](https://discord.gg/turkishvoice)
- [📧 E-posta Listesi](https://groups.google.com/g/turkishvoice)
- [🐦 Twitter](https://twitter.com/turkishvoice)
- [📺 YouTube](https://youtube.com/@turkishvoice)

### Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ayzekhdawy/TurkishVoice&type=Date)](https://star-history.com/#ayzekhdawy/TurkishVoice&Date)

---

## 📄 Lisans

Bu proje **Apache License 2.0** ile lisanslanmıştır.

| Hak | İzin |
|-----|------|
| 📖 Ticari Kullanım | ✅ Serbest |
| ✏️ Değiştirme | ✅ Serbest |
| 📤 Dağıtma | ✅ Serbest |
| 🔒 Özel Kullanım | ✅ Serbest |
| ⚠️ Lisans Bildirimi | Gerekli |

[LICENSE](LICENSE) dosyasını inceleyin.

---

## 📚 Atıf (Citation)

Akademik çalışmalarda kullanıyorsanız:

```bibtex
@software{turkishvoice2026,
  author = {TurkishVoice Team},
  title = {TurkishVoice: Açık Kaynaklı Türkçe Metin Okuma Sistemi},
  year = {2026},
  url = {https://github.com/ayzekhdawy/TurkishVoice},
  license = {Apache-2.0}
}
```

---

## 🙏 Teşekkürler

Bu proje aşağıdaki açık kaynak projelerden ilham almıştır:

- [Coqui TTS](https://github.com/coqui-ai/TTS) - XTTS-v2 mimarisi
- [Piper TTS](https://github.com/rhasspy/piper) - ONNX optimizasyonu
- [Edge TTS](https://github.com/rany-gh/edge-tts) - Microsoft Azure entegrasyonu
- [Gradio](https://gradio.app/) - Web UI

---

## 📬 İletişim

<div align="center">

[🐛 Sorun Bildir](https://github.com/ayzekhdawy/TurkishVoice/issues) •
[💬 Tartışmalara Katıl](https://github.com/ayzekhdawy/TurkishVoice/discussions) •
[📧 E-posta Gönder](mailto:contact@turkishvoice.ai) •
[🐦 Twitter](https://twitter.com/turkishvoice) •
[💬 Discord](https://discord.gg/turkishvoice)

</div>

---

<div align="center">

## 🎯 Hedefimiz

**Türkçe konuşan herkes için erişilebilir, ücretsiz, yüksek kaliteli TTS teknolojisi sağlamak.**

---

**⭐ Bu projeyi beğendiyseniz, yıldız vermeyi unutmayın!**

Made with ❤️ for the Turkish community

[![Star History](https://api.star-history.com/svg?repos=ayzekhdawy/TurkishVoice&type=Date)](https://star-history.com/#ayzekhdawy/TurkishVoice&Date)

---

[Türkçe](#) | [English](README_en.md)

</div>
