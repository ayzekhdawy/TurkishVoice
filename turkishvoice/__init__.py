"""
TurkishVoice - Açık Kaynak Türkçe Metin-Şarkı Sentezi (TTS)

https://github.com/turkishvoice/turkishvoice
"""

__version__ = "0.1.0"
__author__ = "TurkishVoice Team"

from turkishvoice.core.engine import TurkishVoiceEngine
from turkishvoice.turkish.text_normalizer import TurkishTextNormalizer
from turkishvoice.turkish.g2p import TurkishG2P
from turkishvoice.turkish.vowel_harmony import TurkishVowelHarmony
from turkishvoice.turkish.stress_marker import StressMarker

__all__ = [
    "TurkishVoiceEngine",
    "TurkishTextNormalizer",
    "TurkishG2P",
    "TurkishVowelHarmony",
    "StressMarker",
    "__version__",
]
