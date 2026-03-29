"""
Turkish Text Normalizer

Normalizes Turkish text for TTS processing:
- Numbers to words
- Abbreviations expansion
- Punctuation handling
- Capitalization for proper names
- URL and email handling
"""

import re
from typing import List, Dict, Optional, Tuple


class TurkishTextNormalizer:
    """
    Turkish text normalizer for TTS preprocessing.
    """

    # Number words in Turkish
    NUMBER_WORDS: Dict[int, str] = {
        0: 'sifir', 1: 'bir', 2: 'iki', 3: 'uc', 4: 'dort',
        5: 'bes', 6: 'alti', 7: 'yedi', 8: 'sekiz', 9: 'dokuz',
        10: 'on', 11: 'on bir', 12: 'on iki', 13: 'on uc', 14: 'on dort',
        15: 'on bes', 16: 'on alti', 17: 'on yedi', 18: 'on sekiz', 19: 'on dokuz',
        20: 'yirmi', 30: 'otuz', 40: 'kirik', 50: 'elli', 60: 'altmis',
        70: 'yetmis', 80: 'seksen', 90: 'doksan', 100: 'yuz',
        1000: 'bin', 1000000: 'milyon', 1000000000: 'milyar',
    }

    # Common abbreviations
    ABBREVIATIONS: Dict[str, str] = {
        'dr.': 'doktor', 'dr': 'doktor',
        'prof.': 'profesor', 'prof': 'profesor',
        'bknz.': 'bakiniz', 'bknz': 'bakiniz',
        'vb.': 've benzeri', 'vd.': 've digerleri',
        'nr.': 'numara', 'no.': 'numara', 'no': 'numara',
        'apt.': 'apartman', 'sk.': 'sokak', 'cd.': 'caddesi',
        'mr.': 'mister', 'mrs.': 'misess', 'ms.': 'miss',
    }

    # Turkish month names
    MONTHS: Dict[str, str] = {
        'ocak': 'ocak', 'subat': 'subat', 'mart': 'mart',
        'nisan': 'nisan', 'mayis': 'mayis', 'haziran': 'haziran',
        'temmuz': 'temmuz', 'agustos': 'agustos', 'eylul': 'eylul',
        'ekim': 'ekim', 'kasim': 'kasim', 'aralik': 'aralik',
    }

    def __init__(self):
        """Initialize the text normalizer."""
        pass

    def normalize(self, text: str) -> str:
        """
        Normalize Turkish text for TTS.

        Args:
            text: Raw Turkish text

        Returns:
            Normalized text ready for TTS processing
        """
        text = self._expand_abbreviations(text)
        text = self._expand_numbers(text)
        text = self._handle_urls_and_emails(text)
        text = self._normalize_whitespace(text)
        text = self._handle_punctuation(text)

        return text

    def _expand_abbreviations(self, text: str) -> str:
        """Expand common Turkish abbreviations."""
        for abbrev, expansion in self.ABBREVIATIONS.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(abbrev), re.IGNORECASE)
            text = pattern.sub(expansion, text)
        return text

    def _expand_numbers(self, text: str) -> str:
        """
        Convert numbers to Turkish words.

        Handles:
        - Cardinal numbers (1-1000+)
        - Ordinal numbers (1., 2., etc.)
        - Years (2024 -> yirmi dort)
        - Phone numbers
        - Decimal numbers
        """
        # Simple cardinal number conversion (0-99)
        def number_to_words(match):
            num = int(match.group())
            return self._number_to_turkish_words(num)

        # Replace numbers in text
        text = re.sub(r'\b(\d+)\b', number_to_words, text)

        # Handle years specially (e.g., 2024 -> yirmi dort)
        text = re.sub(r'\b(1[0-9]{3})\b', self._year_to_words, text)
        text = re.sub(r'\b(20[0-2][0-9])\b', self._year_to_words, text)

        # Handle ordinal numbers (1., 2., etc.)
        text = re.sub(r'(\d+)\.', lambda m: self._ordinal_to_words(int(m.group(1))), text)

        return text

    def _number_to_turkish_words(self, num: int) -> str:
        """Convert a number to Turkish words."""
        if num in self.NUMBER_WORDS:
            return self.NUMBER_WORDS[num]

        if num < 100:
            tens = (num // 10) * 10
            ones = num % 10
            if ones == 0:
                return self.NUMBER_WORDS[tens]
            return f"{self.NUMBER_WORDS[tens]} {self.NUMBER_WORDS[ones]}"

        if num < 1000:
            hundreds = num // 100
            remainder = num % 100
            if hundreds == 1:
                result = 'yuz'
            else:
                result = f"{self.NUMBER_WORDS[hundreds]} yuz"
            if remainder > 0:
                result += f" {self._number_to_turkish_words(remainder)}"
            return result

        if num < 1000000:
            thousands = num // 1000
            remainder = num % 1000
            if thousands == 1:
                result = 'bin'
            else:
                result = f"{self._number_to_turkish_words(thousands)} bin"
            if remainder > 0:
                result += f" {self._number_to_turkish_words(remainder)}"
            return result

        # Larger numbers
        return str(num)  # Fallback

    def _year_to_words(self, match) -> str:
        """Convert a year to Turkish words."""
        year = int(match.group())
        return self._number_to_turkish_words(year)

    def _ordinal_to_words(self, num: int) -> str:
        """Convert an ordinal number to Turkish words."""
        ordinal_base = self._number_to_turkish_words(num)
        # Ordinal suffix based on vowel harmony
        last_vowel = self._find_last_vowel(ordinal_base)
        if last_vowel in 'aeiou':
            if last_vowel in 'aou':
                return f"{ordinal_base}inci"
            else:
                return f"{ordinal_base}inci"
        return f"{ordinal_base}inci"

    def _find_last_vowel(self, word: str) -> Optional[str]:
        """Find the last vowel in a word."""
        vowels = 'aeiou'
        for char in reversed(word.lower()):
            if char in vowels:
                return char
        return None

    def _handle_urls_and_emails(self, text: str) -> str:
        """Convert URLs and emails to speakable format."""
        # Email: example@mail.com -> example at mail dot com
        email_pattern = r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})'
        text = re.sub(
            email_pattern,
            lambda m: f"{m.group(1).replace('.', ' nokta ')} at {m.group(2)} dot {m.group(3)}",
            text
        )

        # URL: https://example.com -> h t t p s colon slash slash example dot com
        url_pattern = r'https?://[^\s]+'
        def url_to_speech(url):
            # Simple pronunciation guide
            url = url.replace('https://', '')
            url = url.replace('http://', '')
            url = url.replace('/', ' slash ')
            url = url.replace('.', ' dot ')
            return url

        text = re.sub(url_pattern, url_to_speech, text)
        return text

    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace and line breaks."""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        # Replace newlines with spaces
        text = re.sub(r'\n+', ' ', text)
        # Trim leading/trailing whitespace
        text = text.strip()
        return text

    def _handle_punctuation(self, text: str) -> str:
        """
        Handle punctuation for natural speech.

        - Split on sentence endings for natural pauses
        - Mark questions with intonation cues
        - Handle exclamation for emphasis
        """
        # Add pause markers after sentence endings
        text = re.sub(r'([.!?])', r'\1 ', text)
        # Normalize quotes - replace various quote characters with space
        for quote_char in ['"', '"', '"', '"', "'", "'", "'", '"', '„']:
            text = text.replace(quote_char, ' ')
        return text

    def segment_sentences(self, text: str) -> List[str]:
        """
        Segment text into sentences.

        Args:
            text: Input text

        Returns:
            List of sentences
        """
        # Split on sentence-ending punctuation
        sentences = re.split(r'([.!?]+)', text)

        # Recombine punctuation with sentences
        result = []
        current = ''
        for segment in sentences:
            current += segment
            if segment in '.!?':
                if current.strip():
                    result.append(current.strip())
                current = ''

        if current.strip():
            result.append(current.strip())

        return result


def demo():
    """Demonstrate text normalization."""
    print("Turkish Text Normalizer Demo")
    print("=" * 60)

    normalizer = TurkishTextNormalizer()

    test_cases = [
        "Bugun 25 derece ve 2024 yilindayiz.",
        "Dr. Ahmet geliyor. Bknz. sayfa 5.",
        "example@mail.com adresinden ulasabilirsiniz.",
        "Toplam 1.234.567 TL.",
        "Prof. Dr. Yilmaz geliyor!",
    ]

    print("\nInput -> Normalized Output")
    print("-" * 60)

    for text in test_cases:
        normalized = normalizer.normalize(text)
        print(f"\nInput:     {text}")
        print(f"Normalized: {normalized}")

    print("\n" + "=" * 60)
    print("\nSentence segmentation:")
    text = "Merhaba! Nasilsin? Iyiyim tesekkur ederim."
    sentences = normalizer.segment_sentences(text)
    for i, s in enumerate(sentences):
        print(f"  {i+1}. {s}")


if __name__ == "__main__":
    demo()
