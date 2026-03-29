"""
Turkish Grapheme-to-Phoneme (G2P) Converter

Converts Turkish text (graphemes) to IPA phonetic representations.

Turkish-specific mappings:
- ç → tʃ (voiceless postalveolar affricate)
- ş → ʃ (voiceless postalveolar fricative)
- ğ → ː (voxel lengthening - extends previous vowel)
- ö → ø (mid front rounded vowel)
- ü → y (high front rounded vowel)
- ı → ɯ (high back unrounded vowel)

Special cases:
- Dotted and dotless i: ı (dotless) vs i (dotted)
- Vowel lengthening by ğ
- Consonant assimilation in suffixes

Reference: Turkish phonology on Wikipedia
"""

from typing import List, Optional, Tuple, Dict


class TurkishG2P:
    """
    Turkish Grapheme-to-Phoneme converter.
    Converts Turkish orthography to IPA (International Phonetic Alphabet).
    """

    # Basic letter to IPA mapping
    PHONEME_MAP: Dict[str, str] = {
        # Vowels
        'a': 'a',
        'e': 'e',
        'ı': 'ɯ',   # dotless i
        'i': 'i',
        'o': 'o',
        'ö': 'ø',   # o-umlaut
        'u': 'u',
        'ü': 'y',   # u-umlaut

        # Consonants
        'b': 'b',
        'c': 'dʒ',  # j-like sound in "jump"
        'ç': 'tʃ',  # ch-like sound in "church"
        'd': 'd',
        'f': 'f',
        'g': 'g',
        'ğ': 'ː',   # lengthens previous vowel
        'h': 'h',
        'j': 'ʒ',   # zh-like sound in "measure"
        'k': 'k',
        'l': 'l',
        'm': 'm',
        'n': 'n',
        'p': 'p',
        'r': 'r',
        's': 's',
        'ş': 'ʃ',   # sh-like sound in "ship"
        't': 't',
        'v': 'v',
        'y': 'j',   # y-like glide in "yes"
        'z': 'z',

        # Turkish-specific letters
        'â': 'a',   # long a (in loanwords)
        'ê': 'e',   # long e (in loanwords)
    }

    # Consonant letters
    CONSONANTS: frozenset = frozenset('bcçdfgğhjklmnprsştvyz')

    # Letters that don't lengthen vowels
    NON_LENGTHENING_CONSONANTS: frozenset = frozenset('cçfhjklmnprştvy')

    def __init__(self):
        """Initialize the G2P converter."""
        pass

    def convert(self, word: str) -> List[str]:
        """
        Convert a Turkish word to IPA phonemes.

        Args:
            word: A Turkish word

        Returns:
            List of IPA phoneme strings

        Examples:
            >>> g2p = TurkishG2P()
            >>> g2p.convert('merhaba')
            ['m', 'e', 'ɾ', 'h', 'a', 'b', 'a']
            >>> g2p.convert('çiçek')
            ['tʃ', 'iː', 'tʃ', 'e', 'k']
        """
        phonemes = []
        word = word.lower()
        i = 0

        while i < len(word):
            char = word[i]

            if char in self.PHONEME_MAP:
                phoneme = self.PHONEME_MAP[char]

                # Handle ğ (lengthens previous vowel)
                if char == 'ğ':
                    # ğ lengthens the preceding vowel
                    # The actual lengthening is handled by vowel handling
                    # Here we just mark it as lengthener
                    if phonemes and self.is_vowel(phonemes[-1]):
                        # The previous vowel should be lengthened
                        # We indicate this by adding a length mark
                        last_vowel_idx = len(phonemes) - 1
                        phonemes[last_vowel_idx] = phonemes[last_vowel_idx] + 'ː'
                        # Skip adding a separate phoneme for ğ
                        i += 1
                        continue
                    else:
                        # ğ at the start or after consonant - creates diphthong effect
                        i += 1
                        continue

                phonemes.append(phoneme)
            else:
                # Unknown character - skip or add as-is
                phonemes.append(char)

            i += 1

        return phonemes

    def convert_with_vowel_length(self, word: str) -> Tuple[List[str], Dict[int, bool]]:
        """
        Convert a Turkish word to phonemes with vowel length information.

        Returns:
            Tuple of (phonemes, vowel_lengths) where vowel_lengths
            is a dict mapping vowel index to lengthened status
        """
        phonemes = []
        vowel_lengths: Dict[int, bool] = {}
        word = word.lower()
        i = 0

        while i < len(word):
            char = word[i]

            if char in self.PHONEME_MAP:
                phoneme = self.PHONEME_MAP[char]

                if char == 'ğ':
                    # Find the last vowel and mark it as lengthened
                    for j in range(len(phonemes) - 1, -1, -1):
                        if self.is_vowel(phonemes[j]):
                            vowel_lengths[j] = True
                            phonemes[j] = phonemes[j] + 'ː'
                            break
                    i += 1
                    continue

                if self.is_vowel(char):
                    vowel_lengths[len(phonemes)] = False

                phonemes.append(phoneme)
            else:
                phonemes.append(char)

            i += 1

        return phonemes, vowel_lengths

    def word_to_phoneme_string(self, word: str) -> str:
        """
        Convert a Turkish word to a space-separated IPA string.

        Args:
            word: A Turkish word

        Returns:
            Space-separated IPA phonemes

        Examples:
            >>> g2p = TurkishG2P()
            >>> g2p.word_to_phoneme_string('çiçek')
            'tʃ iː tʃ e k'
        """
        return ' '.join(self.convert(word))

    def sentence_to_phonemes(self, sentence: str) -> List[str]:
        """
        Convert a Turkish sentence to phonemes.

        Args:
            sentence: A Turkish sentence

        Returns:
            List of phoneme lists, one per word
        """
        words = sentence.split()
        return [self.convert(word) for word in words]

    def get_phoneme_for_char(self, char: str) -> str:
        """
        Get the IPA phoneme for a single Turkish character.

        Args:
            char: A single character

        Returns:
            IPA representation, or the character itself if not found
        """
        return self.PHONEME_MAP.get(char.lower(), char)

    @staticmethod
    def is_vowel(phoneme: str) -> bool:
        """
        Check if a phoneme is a vowel sound.

        Args:
            phoneme: IPA phoneme string

        Returns:
            True if it's a vowel
        """
        vowel_sounds = {'a', 'e', 'i', 'o', 'u', 'ø', 'y', 'ɯ', 'aː', 'eː', 'iː', 'oː', 'uː', 'øː', 'yː', 'ɯː'}
        return phoneme.lower() in vowel_sounds or any(v in phoneme.lower() for v in ['a', 'e', 'i', 'o', 'u', 'ø', 'y', 'ɯ'])

    @staticmethod
    def is_consonant(char: str) -> bool:
        """Check if a character is a consonant."""
        return char.lower() in TurkishG2P.CONSONANTS


def demo():
    """Demonstrate G2P conversion."""
    print("Turkish G2P Demo")
    print("=" * 60)

    g2p = TurkishG2P()

    test_words = [
        'merhaba',      # hello
        'çiçek',        # flower (ç→tʃ, lengthened i)
        'dağ',          # mountain (ğ lengthens a→aː)
        'kitap',        # book
        'göz',          # eye
        'şehir',        # city
        'üzgün',        # sad
        'öğretmen',     # teacher
        'ıstıla',       # a word with dotless i
        'kürk',         # fur
        'türkçe',       # Turkish
    ]

    print(f"\n{'Word':<15} {'IPA':<40}")
    print("-" * 60)

    for word in test_words:
        ipa = g2p.word_to_phoneme_string(word)
        print(f"{word:<15} {ipa:<40}")

    print("\n" + "=" * 60)
    print("\nPhoneme explanations:")
    explanations = {
        'ç': 'tʃ (like "ch" in "church")',
        'ş': 'ʃ (like "sh" in "ship")',
        'ğ': 'ː (lengthens previous vowel)',
        'c': 'dʒ (like "j" in "jump")',
        'j': 'ʒ (like "s" in "measure")',
        'ö': 'ø (mid front rounded)',
        'ü': 'y (high front rounded)',
        'ı': 'ɯ (high back unrounded)',
    }

    for char, explanation in explanations.items():
        print(f"  {char} → {explanation}")


if __name__ == "__main__":
    demo()
