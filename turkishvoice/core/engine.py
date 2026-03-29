"""
Core TTS engine module.

This module provides the main TurkishVoiceEngine class that orchestrates
the entire TTS pipeline using real neural TTS models (Piper TTS, Edge TTS).
"""

import numpy as np
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
import logging

from turkishvoice.turkish.text_normalizer import TurkishTextNormalizer
from turkishvoice.turkish.g2p import TurkishG2P
from turkishvoice.turkish.vowel_harmony import TurkishVowelHarmony
from turkishvoice.turkish.stress_marker import StressMarker
from turkishvoice.core.piper_engine import PiperTTSVoice, EdgeTTSVoice
from turkishvoice.utils.model_downloader import get_voice_path, download_voice

logger = logging.getLogger(__name__)


class TurkishVoiceEngine:
    """
    Main Turkish Text-to-Speech engine.

    Uses Piper TTS (offline, fast) or Edge TTS (online, high quality)
    for real neural speech synthesis.

    Usage:
        engine = TurkishVoiceEngine(voice='dfki')
        audio = engine.synthesize("Merhaba Türkiye")
        engine.save(audio, "output.wav")
    """

    # Supported output formats
    SUPPORTED_FORMATS = ['wav', 'mp3', 'ogg']

    def __init__(
        self,
        voice: str = "dfki",
        model_path: Optional[str] = None,
        use_piper: bool = True,
        use_edge: bool = False,
        sample_rate: int = 22050,
    ):
        """
        Initialize the TurkishVoice TTS engine.

        Args:
            voice: Voice identifier
                   - Piper: 'dfki', 'fahrettin', 'fettah'
                   - Edge: 'emel', 'ahmet'
            model_path: Path to model weights (optional, auto-downloads)
            use_piper: Use Piper TTS (offline, fast, ~63MB model)
            use_edge: Use Edge TTS (online, high quality, requires internet)
            sample_rate: Audio sample rate for output
        """
        self.voice_name = voice
        self.model_path = model_path
        self.use_piper = use_piper
        self.use_edge = use_edge
        self.use_onnx = True  # Default for compatibility
        self.sample_rate = sample_rate

        # Initialize Turkish text processing components
        self.normalizer = TurkishTextNormalizer()
        self.g2p = TurkishG2P()
        self.vowel_harmony = TurkishVowelHarmony()
        self.stress_marker = StressMarker()

        # TTS engine instances
        self._piper_voice: Optional[PiperTTSVoice] = None
        self._edge_voice: Optional[EdgeTTSVoice] = None
        self._is_loaded = False

        logger.info("TurkishVoice engine initialized")

    @property
    def is_loaded(self) -> bool:
        """Check if the model is loaded."""
        return self._is_loaded

    def load(self):
        """
        Load the TTS model.

        Downloads the model if not already present.
        """
        if self._is_loaded:
            return

        logger.info("Loading TurkishVoice model...")

        # Try Edge TTS first if requested
        if self.use_edge:
            # Initialize Edge TTS
            self._edge_voice = EdgeTTSVoice(voice=self.voice_name)
            self._edge_voice.load()
            self._is_loaded = True
            logger.info(f"Edge TTS voice '{self.voice_name}' initialized")

        # Try Piper TTS if requested
        if self.use_piper:
            # Initialize Piper TTS
            try:
                # Get or download model path
                if self.model_path:
                    model_path = Path(self.model_path)
                else:
                    model_path = get_voice_path(self.voice_name)
                    if model_path is None:
                        logger.info(f"Downloading voice '{self.voice_name}'...")
                        model_path = download_voice(self.voice_name)

                if model_path and Path(model_path).exists():
                    self._piper_voice = PiperTTSVoice(
                        voice=self.voice_name,
                        model_path=model_path,
                        sample_rate=self.sample_rate,
                    )
                    self._piper_voice.load()
                    self._is_loaded = True
                    logger.info(f"Piper voice '{self.voice_name}' loaded successfully")
                else:
                    logger.warning(f"Model not found at {model_path}")

            except ImportError as e:
                logger.error(f"Piper TTS not installed: {e}")
                raise
            except Exception as e:
                logger.error(f"Failed to load Piper voice: {e}")
                raise

        if not self._is_loaded:
            logger.warning("No TTS backend selected. Use use_piper=True or use_edge=True")

        logger.info("Model loaded successfully")

    def _ensure_loaded(self):
        """Ensure the model is loaded before synthesis."""
        if not self._is_loaded:
            self.load()

    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        speed: float = 1.0,
        pitch: float = 1.0,
        prosody_scale: float = 1.0,
    ) -> np.ndarray:
        """
        Synthesize speech from Turkish text.

        Args:
            text: Turkish text to synthesize (max ~5000 characters)
            voice: Voice identifier (overrides default)
            speed: Speech rate (0.5 - 2.0, default 1.0)
            pitch: Pitch multiplier (0.5 - 2.0, default 1.0)
            prosody_scale: Prosody emphasis (not used in Piper)

        Returns:
            Audio waveform as numpy array (float32, mono)

        Raises:
            ValueError: If text is empty or parameters are out of range
        """
        self._ensure_loaded()

        # Validate inputs
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        if not 0.5 <= speed <= 2.0:
            raise ValueError("Speed must be between 0.5 and 2.0")

        if not 0.5 <= pitch <= 2.0:
            raise ValueError("Pitch must be between 0.5 and 2.0")

        logger.info(f"Synthesizing: {text[:50]}{'...' if len(text) > 50 else ''}")

        # Use Piper TTS
        if self.use_piper and self._piper_voice:
            waveform = self._piper_voice.synthesize(
                text=text,
                speed=speed,
                pitch=pitch,
            )
        # Use Edge TTS
        elif self.use_edge and self._edge_voice:
            waveform = self._edge_voice.synthesize(
                text=text,
                speed=speed,
                pitch=pitch,
            )
        else:
            raise RuntimeError("No TTS backend loaded")

        # Normalize audio
        waveform = self._normalize_audio(waveform)

        logger.info(f"Synthesis complete: {len(waveform)} samples, {len(waveform)/self.sample_rate:.2f}s")

        return waveform

    @staticmethod
    def _normalize_audio(waveform: np.ndarray) -> np.ndarray:
        """
        Normalize audio to prevent clipping.

        Args:
            waveform: Input audio

        Returns:
            Normalized audio
        """
        max_val = np.abs(waveform).max()
        if max_val > 0:
            waveform = waveform / max_val * 0.95
        return waveform.astype(np.float32)

    def save(self, audio: np.ndarray, path: Union[str, Path], format: str = 'wav'):
        """
        Save audio to file.

        Args:
            audio: Audio waveform
            path: Output file path
            format: Output format ('wav', 'mp3', 'ogg')
        """
        import soundfile as sf

        path = Path(path)
        format = format.lower()

        if format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {format}. Choose from {self.SUPPORTED_FORMATS}")

        # Ensure correct file extension
        if path.suffix.lower() != f'.{format}':
            path = path.with_suffix(f'.{format}')

        # Save audio
        sf.write(str(path), audio, self.sample_rate)
        logger.info(f"Audio saved to: {path}")

    def get_available_voices(self) -> List[Dict[str, Any]]:
        """
        Get list of available voices.

        Returns:
            List of voice dictionaries with id, name, gender, age
        """
        voices = []

        # Add Piper voices
        if self.use_piper:
            piper_voices = [
                {
                    'id': 'dfki',
                    'name': 'DFKI (Medium)',
                    'gender': 'neutral',
                    'age': 'adult',
                    'description': 'Turkish voice by DFKI (Piper TTS, offline)',
                },
                {
                    'id': 'fahrettin',
                    'name': 'Fahrettin (Medium)',
                    'gender': 'male',
                    'age': 'adult',
                    'description': 'Turkish male voice (Piper TTS, offline)',
                },
                {
                    'id': 'fettah',
                    'name': 'Fettah (Medium)',
                    'gender': 'male',
                    'age': 'adult',
                    'description': 'Turkish male voice (Piper TTS, offline)',
                },
            ]
            voices.extend(piper_voices)

        # Add Edge voices
        if self.use_edge:
            edge_voices = [
                {
                    'id': 'emel',
                    'name': 'Emel (Neural)',
                    'gender': 'female',
                    'age': 'adult',
                    'description': 'Turkish female neural voice (Edge TTS, online)',
                },
                {
                    'id': 'ahmet',
                    'name': 'Ahmet (Neural)',
                    'gender': 'male',
                    'age': 'adult',
                    'description': 'Turkish male neural voice (Edge TTS, online)',
                },
            ]
            voices.extend(edge_voices)

        return voices

    def get_engine_info(self) -> Dict[str, Any]:
        """
        Get engine information.

        Returns:
            Dictionary with engine details
        """
        backend = 'piper' if self.use_piper else ('edge' if self.use_edge else 'none')
        return {
            'name': 'TurkishVoice',
            'version': '0.2.0',
            'sample_rate': self.sample_rate,
            'model_type': 'piper_tts' if self.use_piper else ('edge_tts' if self.use_edge else 'none'),
            'vocoder_type': 'hifigan',
            'is_loaded': self._is_loaded,
            'use_onnx': self.use_onnx,
            'backend': backend,
            'voice': self.voice_name,
        }


def demo():
    """Demonstrate the TurkishVoice engine."""
    print("TurkishVoice Engine Demo")
    print("=" * 60)

    # Initialize engine with Piper
    print("\nInitializing Piper TTS...")
    engine = TurkishVoiceEngine(voice='dfki', use_piper=True)

    # Get engine info
    info = engine.get_engine_info()
    print("\nEngine Info:")
    for key, value in info.items():
        print(f"  {key}: {value}")

    # List available voices
    print("\nAvailable Voices:")
    voices = engine.get_available_voices()
    for voice in voices:
        print(f"  [{voice['id']}] {voice['name']} ({voice['gender']}, {voice['age']})")

    # Synthesize demo
    print("\n" + "-" * 60)
    print("\nSynthesizing: 'Merhaba, TurkishVoice!'")

    try:
        audio = engine.synthesize(
            "Merhaba, TurkishVoice ile tanışın!",
            speed=1.0,
            pitch=1.0,
        )

        print(f"Generated {len(audio)} samples ({len(audio)/engine.sample_rate:.2f}s)")

        # Save to file
        output_path = "demo_output.wav"
        engine.save(audio, output_path)
        print(f"Saved to: {output_path}")

    except Exception as e:
        print(f"Error during synthesis: {e}")
        print("\nNote: Run 'turkishvoice download dfki' to download the voice model first.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
