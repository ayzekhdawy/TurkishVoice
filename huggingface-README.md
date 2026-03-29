---
title: TurkishVoice - Türkçe TTS
emoji: 🇹🇷
colorFrom: red
colorTo: blue
sdk: gradio
sdk_version: "4.20.0"
python_version: "3.10"
app_file: demo_app.py
pinned: false
license: apache-2.0
---

# 🇹🇷 TurkishVoice - Türkçe Metin-Şarkı Sentezi

**Açık kaynaklı Türkçe Text-to-Speech sistemi**

[GitHub Repo](https://github.com/ayzekhdawy/TurkishVoice)

## ✨ Özellikler

- 🎙️ **Neural TTS** - Microsoft Azure altyapısı
- ⚡ **Gerçek Zamanlı** - ~1 saniye gecikme
- 🇹🇷 **Türkçe Özel** - Türkçe dil desteği
- 🔊 **İki Ses** - Kadın (Emel) ve Erkek (Ahmet)
- 🎛️ **Hız Kontrolü** - 0.5x - 2.0x arası

## 🎮 Nasıl Kullanılır?

1. **Metin Girin** - Türkçe metni yazın veya örnek cümle seçin
2. **Ses Seçin** - Emel (Kadın) veya Ahmet (Erkek)
3. **Hızı Ayarlayın** - Varsayılan 1.0
4. **Sentezle** - 🔊 butona tıklayın

## 📚 Örnek Cümleler

- "Merhaba dünya! TurkishVoice ile tanışın."
- "Türkçe metin okuma sistemi başarıyla çalışıyor."
- "Yapay zeka teknolojileri hızla gelişmeye devam ediyor."

## 🔧 Teknik Detaylar

| Özellik | Değer |
|---------|-------|
| **Backend** | Edge TTS (Microsoft Azure) |
| **Sesler** | Emel (Kadın), Ahmet (Erkek) |
| **Kalite** | Neural (24kHz) |
| **Gecikme** | ~700-1500ms |

## 💻 Kendi Bilgisayarınızda Çalıştırın

```bash
# Kurulum
pip install turkishvoice gradio edge-tts

# Demo başlat
python demo_app.py

# Veya CLI ile
turkishvoice serve
```

## 📦 PyPI (Yakında)

```bash
pip install turkishvoice
```

## 🤝 Katkıda Bulunma

[GitHub](https://github.com/ayzekhdawy/TurkishVoice) üzerinden katkıda bulunabilirsiniz.

## 📄 Lisans

Apache License 2.0

---

Made with ❤️ for the Turkish community
