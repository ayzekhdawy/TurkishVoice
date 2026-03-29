# 🇹🇷 TurkishVoice

**Açık kaynaklı Türkçe Metin-Şarkı Sentezi (TTS)**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎮 Canlı Demo

**[https://huggingface.co/spaces/ayzek/TurkishVoice](https://huggingface.co/spaces/ayzek/TurkishVoice)**

Demo üzerinden hemen test edebilirsiniz - kurulum gerekmez!

---

## ✨ Özellikler

| Özellik | TurkishVoice | Google TTS | Azure TTS |
|---------|-------------|------------|-----------|
| **Türkçe Ünlü Uyumu** | ✅ | ❌ | ❌ |
| **G2P Dönüşüm** | ✅ | ❌ | ❌ |
| **Vurgu Marker** | ✅ | ❌ | ❌ |
| **Offline Mode** | ✅ | ❌ | ❌ |
| **Voice Cloning** | ✅ | ✅ ($$$) | ✅ ($$$) |
| **Açık Kaynak** | ✅ | ❌ | ❌ |
| **Ücretsiz** | ✅ | ❌ | ❌ |

---

## 🚀 Hızlı Başlangıç

### Kurulum

```bash
pip install turkishvoice
```

### Kullanım

```python
from turkishvoice import TurkishVoiceEngine

# Edge TTS ile (online, yüksek kalite)
engine = TurkishVoiceEngine(voice='emel', use_edge=True)
audio = engine.synthesize("Merhaba dünya!")
engine.save(audio, "output.wav")

# Piper TTS ile (offline, hızlı)
engine = TurkishVoiceEngine(voice='dfki', use_piper=True)
audio = engine.synthesize("Merhaba dünya!")
```

### CLI

```bash
# Sentez yap
turkishvoice synthesize "Merhaba dünya!" -o output.wav --voice emel

# Sesleri listele
turkishvoice voices

# API sunucusu başlat
turkishvoice serve
```

---

## 🎯 Kullanım Senaryoları

### 1. Erişilebilirlik
Görme engelliler için web sitelerini, belgeleri sesli hale getirin.

### 2. İçerik Üretimi
YouTube, TikTok videoları için otomatik seslendirme.

### 3. Eğitim
Ders materyallerini, kitapları sesli hale getirin.

### 4. Call Center / IVR
Telefon sistemleri için Türkçe otomatik yanıt.

---

## 🎙️ Sesler

### Edge TTS (Online - Yüksek Kalite)

| ID | İsim | Cinsiyet |
|----|------|----------|
| `emel` | Emel | Kadın |
| `ahmet` | Ahmet | Erkek |

### Piper TTS (Offline - Hızlı)

| ID | İsim |
|----|------|
| `dfki` | DFKI |

---

## 🔧 API

### REST API

```bash
# Sunucuyu başlat
turkishvoice serve --port 8000

# Sentez yap
curl -X POST "http://localhost:8000/api/v1/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text":"Merhaba","voice":"emel"}' \
  -o output.wav
```

---

## 📦 Bağımlılıklar

```toml
# Temel
numpy>=1.21.0
soundfile>=0.12.0
edge-tts>=6.1.0

# Opsiyonel
piper-tts>=1.2.0        # Offline TTS
coqui-tts>=0.22.0       # Voice cloning
gradio>=4.0.0           # Web UI
```

---

## 🛠️ Geliştirme

```bash
git clone https://github.com/ayzekhdawy/TurkishVoice
cd TurkishVoice
pip install -e ".[all]"
pytest tests/
```

---

## 📄 Lisans

Apache 2.0 - Ticari kullanım serbest.

---

Made with ❤️ for the Turkish community
