# TurkishVoice - Açık Kaynak Türkçe Metin-Şarkı Sentezi

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![Status](https://img.shields.io/badge/Status-Alpha-orange.svg)

> **TurkishVoice**, Türkçe metinleri doğal konuşma sesine dönüştürmek için geliştirilmiş açık kaynaklı bir Text-to-Speech (TTS) motorudur.

## 🔥 Özellikler

- **🏠 Türkçe Öncelikli**: Vowel harmony, stress marking, ve morphological analysis ile Türkçe'ye özel optimize
- **🆓 Tamamen Açık Kaynak**: Apache 2.0 lisansı ile ücretsiz ve ticari kullanım serbest
- **🖥️ CPU-Optimized**: NVIDIA GPU gerektirmez, ONNX ile Intel/AMD CPU'larda verimli çalışır
- **🎭 Voice Cloning**: 10-30 saniye referans ses ile kendi sesinizi oluşturun
- **📦 Çoklu Arayüz**: Python API, CLI, REST API ve Web UI
- **🌐 Çok Dilli Temel**: Mevcut Coqui/Piper altyapısı üzerine inşa edilmiş

## 📦 Kurulum

### pip ile (Tavsiye Edilen)

```bash
pip install turkishvoice
```

### Kaynaktan Derleme

```bash
git clone https://github.com/turkishvoice/turkishvoice.git
cd turkishvoice
pip install -e .
```

### Sistem Gereksinimleri

- Python 3.8+
- 8 GB RAM (minimum), 16 GB önerilen
- Intel i5/i7 veya eşdeğer CPU (veya NVIDIA GPU)

## 🚀 Hızlı Başlangıç

### Python API

```python
from turkishvoice import TurkishVoice

# Motoru başlat
tts = TurkishVoice()

# Sentezle
audio = tts.synthesize("Merhaba, ben TurkishVoice!")
tts.save(audio, "merhaba.wav")
```

### CLI

```bash
# Basit sentez
turkishvoice synthesize "Günaydın Türkiye" -o output.wav

# Farklı ses ile
turkishvoice synthesize "Merhaba" -o merhaba.wav --voice erkek

# Mevcut sesleri listele
turkishvoice voices --list

# Web UI başlat
turkishvoice serve
```

### Web UI

```bash
turkishvoice serve
# http://localhost:7860 adresinde açılır
```

### REST API

```bash
# API sunucu başlat
turkishvoice serve --api

# Sentez isteği
curl -X POST http://localhost:8000/api/v1/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Merhaba", "voice": "default"}'
```

## 🎯 Desteklenen Diller

- **Ana Dil**: Türkçe (tr-TR)
- **Deneysel**: İngilizce (en-US), Almanca (de-DE)

## 📁 Proje Yapısı

```
turkishvoice/
├── turkishvoice/           # Ana Python paketi
│   ├── core/               # TTS motoru
│   ├── turkish/            # Türkçe işleme (vowel harmony, G2P, stress)
│   ├── api/                # FastAPI REST API
│   ├── cli/                # CLI aracı
│   └── utils/              # Yardımcı fonksiyonlar
├── webui/                  # Gradio Web UI
├── training/               # Eğitim scriptleri
├── tests/                  # Testler
└── models/                 # Ön-eğitimli ses modelleri
```

## 🔧 Türkçe İşleme Pipeline

```
Metin → Normalizasyon → Morphological Analiz → G2P → Vowel Harmony → Stress → Prosody → Fonem Dizisi
```

TurkishVoice, Türkçe'nin benzersiz dilbilgisel özelliklerini işlemek için özel olarak tasarlanmış bir pipeline kullanır:

- **Vowel Harmony**: Suffix ünlüleri önceki ünlü ile uyumlu hale getirir (a/ı/o/u ↔ e/i/ö/ü)
- **G2P**: Türkçe grafemlerini IPA fonemlerine dönüştürür (ç→tʃ, ş→ʃ, ğ→ː)
- **Stress Marking**: Türkçe'nin sözcüksel vurgu kurallarını uygular
- **Prosody Prediction**: Doğal konuşma için pitch ve duration tahmini

## 🤝 Katkıda Bulunma

Katkıda bulunmak için lütfen [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını okuyun.

```bash
# Fork edin
# Değişikliklerinizi yapın
# Test edin
pytest tests/

# PR açın
```

## 📜 Lisans

Bu proje Apache License 2.0 ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

Bu proje aşağıdaki açık kaynak projelerden ilham almıştır:

- [Coqui TTS](https://github.com/idiap/coqui-ai-TTS) - XTTS-v2 mimarisi
- [Piper TTS](https://github.com/rhasspy/piper) - ONNX optimizasyonu
- [Bark](https://github.com/suno-ai/bark) - Transform tabanlı TTS
- [Zemberek-NLP](https://github.com/ahmetaa/zemberek-nlp) - Türkçe NLP

## 📬 İletişim

- GitHub Issues: [turkishvoice/turkishvoice/issues](https://github.com/turkishvoice/turkishvoice/issues)
- Discord: [TurkishVoice Community](https://discord.gg/turkishvoice)

---

**⭐ Bu projeyi beğendiyseniz, yıldız vermeyi unutmayın!**
