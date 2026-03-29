"""
Turkish Vowel Harmony Implementation

Turkish vowel harmony is a systematic pattern where suffix vowels harmonize
with the vowel in the root/stem of the word:

- Backness harmony: a/ı/o/u (back) vs e/i/ö/ü (front)
- Roundness harmony: o/ö/u/ü (rounded) vs a/ı/e/i (unrounded)

Examples:
- kitap (book) + -lar (plural) → kitaplar (back vowel 'a')
- kütüphane (library) + -ler (plural) → kütüphaneler (front vowel 'e')
- ev (house) + -im (possessive 1sg) → evim (front vowel 'e')

Reference: https://en.wikipedia.org/wiki/Vowel_harmony#Turkish
"""

from typing import Optional, Tuple


class TurkishVowelHarmony:
    """
    Implements Turkish vowel harmony rules for suffix vowel selection.
    """

    # Turkish vowels classified by backness and roundness
    BACK_VOWELS: frozenset = frozenset('aıou')  # a, ı, o, u
    FRONT_VOWELS: frozenset = frozenset('eiöü')  # e, i, ö, ü
    ROUND_VOWELS: frozenset = frozenset('oöuü')  # o, ö, u, ü
    UNROUND_VOWELS: frozenset = frozenset('aıei')  # a, ı, e, i

    # Turkish alphabet order for vowel classification
    VOWELS: str = 'aeıioöuü'

    def __init__(self):
        """Initialize the vowel harmony processor."""
        pass

    @staticmethod
    def is_vowel(char: str) -> bool:
        """Check if a character is a Turkish vowel."""
        return char.lower() in TurkishVowelHarmony.VOWELS

    @staticmethod
    def get_vowel_class(char: str) -> Optional[str]:
        """
        Return vowel class: 'back', 'front', or None if not a vowel.

        Args:
            char: A single character

        Returns:
            'back' for a/ı/o/u, 'front' for e/i/ö/ü, None otherwise
        """
        char = char.lower()
        if char in TurkishVowelHarmony.BACK_VOWELS:
            return 'back'
        if char in TurkishVowelHarmony.FRONT_VOWELS:
            return 'front'
        return None

    @staticmethod
    def get_roundness(char: str) -> Optional[str]:
        """
        Return roundness class: 'round', 'unround', or None if not a vowel.

        Args:
            char: A single character

        Returns:
            'round' for o/ö/u/ü, 'unround' for a/ı/e/i, None otherwise
        """
        char = char.lower()
        if char in TurkishVowelHarmony.ROUND_VOWELS:
            return 'round'
        if char in TurkishVowelHarmony.UNROUND_VOWELS:
            return 'unround'
        return None

    @staticmethod
    def find_last_vowel(word: str) -> Optional[str]:
        """
        Find the last vowel in a Turkish word (last harmony domain).

        For vowel harmony purposes, we look at the last vowel of the
        root/stem, which is typically the last vowel in the word.

        Args:
            word: A Turkish word

        Returns:
            The last vowel character, or None if no vowel found
        """
        for char in reversed(word.lower()):
            if TurkishVowelHarmony.is_vowel(char):
                return char
        return None

    @staticmethod
    def get_harmony_type(word: str) -> str:
        """
        Determine the harmony type of a word based on its last vowel.

        Args:
            word: A Turkish word

        Returns:
            'back' if last vowel is back (a/ı/o/u),
            'front' if last vowel is front (e/i/ö/ü)
        """
        last_vowel = TurkishVowelHarmony.find_last_vowel(word)
        if last_vowel is None:
            return 'back'  # Default to back if no vowel found
        return TurkishVowelHarmony.get_vowel_class(last_vowel)

    @classmethod
    def harmonize_suffix(cls, suffix: str, preceding_vowel: str) -> str:
        """
        Apply vowel harmony to a suffix based on the preceding vowel.

        This handles both backness and roundness harmony:
        - If preceding vowel is back (a/ı/o/u), use back suffix vowels
        - If preceding vowel is front (e/i/ö/ü), use front suffix vowels
        - Roundness affects high vowels (ı/i, u/ü)

        Args:
            suffix: The suffix to harmonize (e.g., '-ler', '-lar')
            preceding_vowel: The vowel in the word stem to harmonize with

        Returns:
            The suffix with harmonized vowels

        Examples:
            >>> cls.harmonize_suffix('-ler', 'a')
            '-lar'
            >>> cls.harmonize_suffix('-ler', 'e')
            '-ler'
            >>> cls.harmonize_suffix('-iy', 'a')
            '-iy'
            >>> cls.harmonize_suffix('-iy', 'e')
            '-iy'
        """
        if not preceding_vowel:
            return suffix

        harmony_type = cls.get_vowel_class(preceding_vowel)
        if harmony_type is None:
            return suffix

        # Vowel mapping for harmony transformation
        # Backness: a↔e, ı↔i, o↔ö, u↔ü
        # If preceding vowel is back, suffix vowels should be back (e→a, i→ı, ö→o, ü→u)
        # If preceding vowel is front, suffix vowels should be front (a→e, ı→i, o→ö, u→ü)
        if harmony_type == 'back':
            # Convert front vowels in suffix to back vowels
            vowel_map = {'e': 'a', 'i': 'ı', 'ö': 'o', 'ü': 'u'}
        else:
            # Convert back vowels in suffix to front vowels
            vowel_map = {'a': 'e', 'ı': 'i', 'o': 'ö', 'u': 'ü'}

        result = []
        for char in suffix:
            if char.lower() in vowel_map:
                # Apply harmony transformation
                mapped = vowel_map[char.lower()]
                # Preserve original case
                if char.isupper():
                    mapped = mapped.upper()
                result.append(mapped)
            else:
                result.append(char)

        return ''.join(result)

    @classmethod
    def harmonize_word(cls, root: str, suffix: str) -> str:
        """
        Combine a root with a harmonized suffix.

        Args:
            root: The word root
            suffix: The suffix to attach (will be harmonized)

        Returns:
            The root + harmonized suffix

        Examples:
            >>> cls.harmonize_word('kitap', '-lar')
            'kitaplar'
            >>> cls.harmonize_word('kütüphan', '-ler')
            'kütüphaneler'
            >>> cls.harmonize_word('ev', '-im')
            'evim'
        """
        last_vowel = cls.find_last_vowel(root)
        harmonized = cls.harmonize_suffix(suffix, last_vowel)
        # Remove leading '-' from suffix if present
        if harmonized.startswith('-'):
            harmonized = harmonized[1:]
        return root + harmonized

    @staticmethod
    def get_vowel_info(char: str) -> dict:
        """
        Get detailed vowel classification information.

        Args:
            char: A single character

        Returns:
            Dictionary with 'is_vowel', 'class', and 'roundness' keys
        """
        char = char.lower()
        return {
            'is_vowel': char in TurkishVowelHarmony.VOWELS,
            'class': TurkishVowelHarmony.get_vowel_class(char),
            'roundness': TurkishVowelHarmony.get_roundness(char),
        }


def demo():
    """Demonstrate vowel harmony rules."""
    print("Turkish Vowel Harmony Demo")
    print("=" * 50)

    harmony = TurkishVowelHarmony()

    # Test cases
    test_cases = [
        ('kitap', '-lar', 'kitaplar'),
        ('kütüphan', '-ler', 'kütüphaneler'),
        ('ev', '-im', 'evim'),
        ('kız', '-ım', 'kızım'),
        ('elma', '-ler', 'elmeler'),
        ('kapı', '-lar', 'kapılar'),
        ('ördek', '-ler', 'ördekler'),
        ('su', '-lar', 'sular'),
        ('göz', '-ler', 'gözler'),
        ('dağ', '-lar', 'dağlar'),
    ]

    print(f"\n{'Word':<15} {'+ Suffix':<10} {'Result':<15} {'Expected':<15} {'OK?'}")
    print("-" * 65)

    for root, suffix, expected in test_cases:
        result = harmony.harmonize_word(root, suffix)
        ok = "✓" if result == expected else "✗"
        print(f"{root:<15} {suffix:<10} {result:<15} {expected:<15} {ok}")

    print("\n" + "=" * 50)
    print("Vowel classification examples:")
    for vowel in 'aeıioöuü':
        info = harmony.get_vowel_info(vowel)
        print(f"  {vowel}: backness={info['class']}, roundness={info['roundness']}")


if __name__ == "__main__":
    demo()
