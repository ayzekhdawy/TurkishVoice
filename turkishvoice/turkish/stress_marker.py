"""
Turkish Stress Marker

Turkish has a primarily lexical stress system - most words have stress
on the last syllable by default. However, certain suffixes and grammatical
markers can affect stress placement.

Default Rule:
- Primary stress on the last syllable of simple words

Prestressing Suffixes (vurgulu ek):
- Certain suffixes carry their own stress
- When attached, stress moves to the suffix syllable

Unstressed Suffixes (ünsüz ek):
- Some suffixes never receive stress
- Stress remains on the root

Key Examples:
- kitap (book) → KA-tap (stress on first syllable in some dialects)
- ev (house) → ev (no change needed)
- gidiyor (going) → gi-Dİ-yor (prestressing -yor)
- geliyorum (I come) → ge-Lİ-yorum (prestressing -yor with harmony)
- evim (my house) → e-VİM (possessive gets stress)
- kitaplar (books) → ki-TAP-lar (stress remains on root)

Reference: Göksel & Kerslake (2005), Turkish: A Comprehensive Grammar
"""

from typing import List, Optional, Tuple


class StressMarker:
    """
    Turkish stress marker for TTS prosody generation.
    """

    # Suffixes that carry their own stress (prestressing suffixes)
    PRESTRESSING_SUFFIXES: frozenset = frozenset([
        '-yor',      # progressive: gidiyor (going)
        '-yardım',   # helper: yardım (help)
        '-mış',      # indirect evidence: gelmiş (apparently came)
        '-cek',      # future: gelecek (will come)
        '-caktır',   # definite future
        '-sığ',      # ability: gelebilirim (I can come)
        '-yebil',    # ability variant
        '-yemez',    # inability
        '-yazır',    # may accidentally
        '-malı',     # obligation: gelmeli (must come)
        '-meli',     # obligation variant
    ])

    # Suffixes that never receive stress
    UNSTRESSED_SUFFIXES: frozenset = frozenset([
        '-de', '-den',  # locative/ablative: evde (at home)
        '-e', '-a',     # dative: eve (to house)
        '-la', '-le',   # instrumental: evle (with house)
        '-lık', '-lik', # suffix forming nouns: güzel (beautiful)
        '-ca', '-ce',   # comparative: Türkçe (Turkish)
        '-cı', '-ci',   # occupation: öğretmen (teacher)
        '-cıl', '-cil', # occupational variant
        '-lı', '-li',   # possessive: Ankaralı (from Ankara)
        '-lu', '-lü',   # possessive variant
        '-nu', '-nü',   # 3rd person possessive
        '-nun', '-nün', # 3rd person possessive variant
        '-ım', '-im',   # 1st person singular possessive
        '-ın', '-in',   # 1st person singular possessive variant
        '-si', '-sı',   # 3rd person singular possessive
        '-sin', '-sın', # 2nd person singular possessive
    ])

    # Simple vowels for syllable counting
    VOWELS: str = 'aeıioöuü'

    def __init__(self):
        """Initialize the stress marker."""
        pass

    def count_syllables(self, word: str) -> int:
        """
        Count the number of syllables in a Turkish word.

        A syllable is typically one vowel plus following consonants.
        Turkish syllables are (C)V(C)(C) pattern.

        Args:
            word: A Turkish word

        Returns:
            Number of syllables
        """
        count = 0
        for char in word.lower():
            if char in self.VOWELS:
                count += 1
        return max(1, count)

    def get_syllable_boundaries(self, word: str) -> List[int]:
        """
        Get the starting index of each syllable in a word.

        Args:
            word: A Turkish word

        Returns:
            List of starting indices for each syllable
        """
        boundaries = [0]
        vowel_count = 0

        for i, char in enumerate(word.lower()):
            if char in self.VOWELS:
                vowel_count += 1
                if vowel_count > 1:
                    boundaries.append(i)

        return boundaries

    def get_default_stress_position(self, word: str) -> int:
        """
        Get the default stress position for a simple word.

        Default: stress on the last syllable (for Turkish).

        Args:
            word: A Turkish word

        Returns:
            Syllable index that should receive stress (0-indexed from start)
        """
        syllables = self.count_syllables(word)
        # Default: last syllable
        return syllables - 1

    def is_prestressing_suffix(self, suffix: str) -> bool:
        """
        Check if a suffix is a prestressing suffix (carries its own stress).

        Args:
            suffix: The suffix to check

        Returns:
            True if the suffix carries stress
        """
        suffix_lower = suffix.lower()
        return any(ps in suffix_lower for ps in self.PRESTRESSING_SUFFIXES)

    def is_unstressed_suffix(self, suffix: str) -> bool:
        """
        Check if a suffix is unstressed (never receives stress).

        Args:
            suffix: The suffix to check

        Returns:
            True if the suffix never carries stress
        """
        suffix_lower = suffix.lower()
        return any(us in suffix_lower for us in self.UNSTRESSED_SUFFIXES)

    def get_stress_position(self, word: str, suffixes: Optional[List[str]] = None) -> int:
        """
        Determine the stress position for a word.

        If suffixes are provided, the stress rules for those suffixes
        are applied. Otherwise, default to last-syllable stress.

        Args:
            word: The word to analyze
            suffixes: Optional list of suffixes attached to the word

        Returns:
            Syllable index for stress (0-indexed)
        """
        if suffixes:
            # Check if any suffix is prestressing
            for suffix in suffixes:
                if self.is_prestressing_suffix(suffix):
                    # Find which syllable the suffix starts
                    # For prestressing suffixes, stress moves to the suffix
                    word_syllables = self.count_syllables(
                        word.rsplit('-', 1)[0] if '-' in word else word
                    )
                    return word_syllables  # Stress on suffix syllable

            # Check for unstressed suffixes
            for suffix in suffixes:
                if self.is_unstressed_suffix(suffix):
                    # Stress stays on root
                    return self.get_default_stress_position(word)

        # Default: stress last syllable
        return self.get_default_stress_position(word)

    def mark_stress(self, word: str, stress_position: Optional[int] = None) -> str:
        """
        Mark stress position in a word with IPA stress markers.

        Args:
            word: The word to mark
            stress_position: Optional specific stress position

        Returns:
            Word with stress markers (' before stressed syllable)
        """
        if stress_position is None:
            stress_position = self.get_stress_position(word)

        syllables = self.get_syllable_boundaries(word)

        if stress_position >= len(syllables):
            stress_position = len(syllables) - 1

        # Insert stress marker at the start of the stressed syllable
        stress_idx = syllables[stress_position]

        # IPA stress marker: ˈ (primary stress)
        marked = word[:stress_idx] + "'" + word[stress_idx:]

        return marked

    def get_prosody_tags(self, word: str) -> dict:
        """
        Get prosody tags for a word (stress, pitch, duration).

        Args:
            word: The word to analyze

        Returns:
            Dictionary with prosodic information
        """
        stress_pos = self.get_stress_position(word)
        syllables = self.count_syllables(word)

        return {
            'word': word,
            'syllables': syllables,
            'stress_position': stress_pos,
            'stress_is_final': stress_pos == syllables - 1,
            'is_monosyllabic': syllables == 1,
        }


def demo():
    """Demonstrate stress marking."""
    print("Turkish Stress Marker Demo")
    print("=" * 60)

    marker = StressMarker()

    test_cases = [
        ('kitap', 'book'),
        ('ev', 'house'),
        ('gidiyor', 'going'),
        ('geliyorum', 'I come'),
        ('evim', 'my house'),
        ('kitaplar', 'books'),
        ('öğretmen', 'teacher'),
        ('Türkçe', 'Turkish'),
        ('Ankara', 'Ankara'),
        ('geliyorsun', 'you are coming'),
    ]

    print(f"\n{'Word':<15} {'Syllables':<10} {'Stress Pos':<12} {'Marked':<15}")
    print("-" * 60)

    for word, meaning in test_cases:
        syllables = marker.count_syllables(word)
        stress_pos = marker.get_stress_position(word)
        marked = marker.mark_stress(word, stress_pos)
        print(f"{word:<15} {syllables:<10} {stress_pos:<12} {marked:<15} ({meaning})")

    print("\n" + "=" * 60)
    print("\nSuffix Types:")
    print("\nPrestressing Suffixes (carry their own stress):")
    for suffix in sorted(marker.PRESTRESSING_SUFFIXES):
        print(f"  {suffix}")

    print("\nUnstressed Suffixes (never receive stress):")
    for suffix in sorted(marker.UNSTRESSED_SUFFIXES)[:10]:
        print(f"  {suffix}")


if __name__ == "__main__":
    demo()
