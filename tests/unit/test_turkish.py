"""Tests for Turkish text processing."""

import pytest
from turkishvoice.turkish.vowel_harmony import TurkishVowelHarmony
from turkishvoice.turkish.g2p import TurkishG2P
from turkishvoice.turkish.stress_marker import StressMarker
from turkishvoice.turkish.text_normalizer import TurkishTextNormalizer


class TestTurkishVowelHarmony:
    """Tests for Turkish vowel harmony."""

    def setup_method(self):
        self.harmony = TurkishVowelHarmony()

    def test_is_vowel(self):
        assert self.harmony.is_vowel('a')
        assert self.harmony.is_vowel('e')
        assert self.harmony.is_vowel('ı')
        assert self.harmony.is_vowel('i')
        assert self.harmony.is_vowel('o')
        assert self.harmony.is_vowel('ö')
        assert self.harmony.is_vowel('u')
        assert self.harmony.is_vowel('ü')
        assert not self.harmony.is_vowel('b')
        assert not self.harmony.is_vowel('c')

    def test_get_vowel_class_back(self):
        assert self.harmony.get_vowel_class('a') == 'back'
        assert self.harmony.get_vowel_class('ı') == 'back'
        assert self.harmony.get_vowel_class('o') == 'back'
        assert self.harmony.get_vowel_class('u') == 'back'

    def test_get_vowel_class_front(self):
        assert self.harmony.get_vowel_class('e') == 'front'
        assert self.harmony.get_vowel_class('i') == 'front'
        assert self.harmony.get_vowel_class('ö') == 'front'
        assert self.harmony.get_vowel_class('ü') == 'front'

    def test_get_vowel_class_non_vowel(self):
        assert self.harmony.get_vowel_class('b') is None
        assert self.harmony.get_vowel_class('c') is None

    def test_find_last_vowel_back(self):
        assert self.harmony.find_last_vowel('kitap') == 'a'
        assert self.harmony.find_last_vowel('ev') == 'e'
        assert self.harmony.find_last_vowel('kapı') == 'ı'

    def test_find_last_vowel_front(self):
        assert self.harmony.find_last_vowel('kütüphan') == 'a'
        assert self.harmony.find_last_vowel('göz') == 'ö'  # Last vowel in 'göz' is 'ö'

    def test_harmonize_suffix_back(self):
        # kitap (ends with 'a' - back) + -ler → -lar
        result = self.harmony.harmonize_suffix('-ler', 'a')
        assert result == '-lar'

    def test_harmonize_suffix_front(self):
        # kütüphan (ends with 'a' but harmony based on preceding vowel)
        # ev (ends with 'e' - front) + -ler → -ler
        result = self.harmony.harmonize_suffix('-ler', 'e')
        assert result == '-ler'

    def test_harmonize_word(self):
        assert self.harmony.harmonize_word('kitap', '-lar') == 'kitaplar'
        assert self.harmony.harmonize_word('ev', '-im') == 'evim'


class TestTurkishG2P:
    """Tests for Turkish G2P conversion."""

    def setup_method(self):
        self.g2p = TurkishG2P()

    def test_convert_simple(self):
        result = self.g2p.convert('kitap')
        assert 'k' in result
        assert 'i' in result
        assert 't' in result
        assert 'a' in result
        assert 'p' in result

    def test_convert_special_chars(self):
        result = self.g2p.convert('çiçek')
        assert 'tʃ' in result  # ç → tʃ

    def test_convert_shat(self):
        result = self.g2p.convert('şehir')
        assert 'ʃ' in result  # ş → ʃ

    def test_word_to_phoneme_string(self):
        result = self.g2p.word_to_phoneme_string('merhaba')
        assert 'm' in result
        assert 'e' in result
        assert 'r' in result or 'ɾ' in result


class TestStressMarker:
    """Tests for Turkish stress marking."""

    def setup_method(self):
        self.marker = StressMarker()

    def test_count_syllables(self):
        assert self.marker.count_syllables('kitap') == 2
        assert self.marker.count_syllables('ev') == 1
        assert self.marker.count_syllables('merhaba') == 3
        assert self.marker.count_syllables('Türkçe') == 2

    def test_get_default_stress_position(self):
        # Default: stress on last syllable
        assert self.marker.get_default_stress_position('kitap') == 1
        assert self.marker.get_default_stress_position('ev') == 0

    def test_is_prestressing_suffix(self):
        assert self.marker.is_prestressing_suffix('-yor')
        assert not self.marker.is_prestressing_suffix('-lar')

    def test_is_unstressed_suffix(self):
        assert self.marker.is_unstressed_suffix('-de')
        assert self.marker.is_unstressed_suffix('-e')
        assert not self.marker.is_unstressed_suffix('-yor')


class TestTextNormalizer:
    """Tests for Turkish text normalizer."""

    def setup_method(self):
        self.normalizer = TurkishTextNormalizer()

    def test_normalize_basic(self):
        result = self.normalizer.normalize('Merhaba!')
        assert 'Merhaba' in result

    def test_expand_abbreviations(self):
        result = self.normalizer._expand_abbreviations('Dr. Ahmet geliyor.')
        assert 'doktor' in result

    def test_normalize_whitespace(self):
        result = self.normalizer._normalize_whitespace('Merhaba    dünya')
        assert '  ' not in result

    def test_segment_sentences(self):
        result = self.normalizer.segment_sentences('Merhaba! Nasılsın? İyiyim.')
        assert len(result) >= 2
