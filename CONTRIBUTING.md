# Katkıda Bulunma Kılavuzu

TurkishVoice projesine katkıda bulunmak ister misin? Harika! 🎉

## Nasıl Katkıda Bulunabilirsin?

### 1. Kod Katkısı

1. **Fork et**: GitHub'da projeyi fork edin
2. **Clone et**: `git clone https://github.com/{username}/turkishvoice.git`
3. **Branch oluştur**: `git checkout -b feature/yeni-ozellik`
4. **Değişiklikleri yap**: Kodunuzu yazın
5. **Test et**: `pytest tests/` ile testleri çalıştırın
6. **Commit et**: `git commit -m "feat: yeni özellik eklendi"`
7. **Push et**: `git push origin feature/yeni-ozellik`
8. **PR aç**: Pull Request oluşturun

### 2. Test Katkısı

- Bir özellik için test yazın
- Mevcut testleri iyileştirin
- Yeni test senaryoları ekleyin

### 3. Dokümantasyon

- README.md'yi iyileştırın
- Docstring'ler ekleyin
- Türkçe/İngilizce dokümantasyon yazın

### 4. Ses Kaydı Katkısı

- Türkçe ses kaydı paylaşın (lisans uyumlu)
- Farklı lehçelerde örnekler sunun

## Kod Standartları

### Python Kodu
- [PEP 8](https://www.python.org/dev/peps/pep-0008/) takip edin
- `black` formatter kullanın
- `isort` ile import'ları düzenleyin

```bash
# Format
black turkishvoice/
isort turkishvoice/

# Lint
flake8 turkishvoice/
```

### Testler
- Her yeni özellik için test yazın
- Mevcut testlerin geçtiğinden emin olun

```bash
# Testleri çalıştır
pytest tests/ -v

# Coverage ile
pytest tests/ --cov=turkishvoice --cov-report=html
```

## Proje Yapısı

```
turkishvoice/
├── turkishvoice/           # Ana paket
│   ├── core/               # TTS motoru
│   ├── turkish/            # Türkçe işleme
│   ├── api/                # REST API
│   ├── cli/                # CLI
│   └── webui/              # Web UI
├── tests/                  # Testler
└── docs/                   # Dokümantasyon
```

## Commit Mesajları

[Conventional Commits](https://www.conventionalcommits.org/) formatını kullanın:

```
feat: yeni özellik
fix: hata düzeltmesi
docs: dokümantasyon değişikliği
style: kod formatı (fonksiyonalite değişikliği yok)
refactor: kod yeniden yapılandırma
test: test ekleme/düzeltme
chore: bakım görevleri
```

Örnekler:
- `feat: Türkçe vowel harmony desteği eklendi`
- `fix: G2P çeviri hatası düzeltildi`
- `docs: README güncellendi`

## Sorularınız mı var?

- GitHub Issues: https://github.com/turkishvoice/turkishvoice/issues
- Discord: https://discord.gg/turkishvoice

## Lisans

Katkıda bulunarak, kodunuzun Apache 2.0 lisansı altında yayınlanacağını kabul etmiş olursunuz.

---

**Teşekkürler!** TurkishVoice'i daha iyi hale getirdiğiniz için 🎉
