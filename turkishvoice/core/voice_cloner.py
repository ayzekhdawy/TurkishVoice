"""
Voice Cloning Module using Coqui XTTS v2

This module allows cloning voices from reference audio samples.
Requires: pip install coqui-tts
"""

import numpy as np
from pathlib import Path
from typing import Optional, Union
import logging
import tempfile

logger = logging.getLogger(__name__)


class VoiceCloner:
    """
    Voice cloner using Coqui XTTS v2.

    XTTS v2 can clone voices from just 6+ seconds of reference audio.
    Supports Turkish language natively.
    """

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the voice cloner.

        Args:
            model_path: Optional path to XTTS v2 model (downloads if not provided)
        """
        self.model_path = model_path
        self._tts = None
        self._is_loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def load(self):
        """Load the XTTS v2 model."""
        if self._is_loaded:
            return

        try:
            from TTS.api import TTS

            logger.info("Loading Coqui XTTS v2 model...")

            # Use multilingual XTTS v2
            model_name = "tts_models/multilingual/multi-dataset/xtts_v2"

            if self.model_path:
                self._tts = TTS(model_path=self.model_path)
            else:
                self._tts = TTS(model_name)

            self._is_loaded = True
            logger.info("XTTS v2 model loaded successfully")

        except ImportError:
            raise ImportError(
                "Coqui TTS is not installed. "
                "Run: pip install coqui-tts"
            )
        except Exception as e:
            logger.error(f"Failed to load XTTS model: {e}")
            raise

    def _ensure_loaded(self):
        if not self._is_loaded:
            self.load()

    def clone(
        self,
        reference_audio: Union[str, Path],
        text: str,
        language: str = "tr",
        output_path: Optional[Union[str, Path]] = None,
    ) -> np.ndarray:
        """
        Clone a voice from reference audio and synthesize text.

        Args:
            reference_audio: Path to reference audio file (WAV, MP3, etc.)
                           Should be 6+ seconds of clear speech
            text: Text to synthesize with cloned voice
            language: Language code (default: 'tr' for Turkish)
            output_path: Optional path to save output audio

        Returns:
            Audio waveform as numpy array
        """
        self._ensure_loaded()

        reference_audio = Path(reference_audio)
        if not reference_audio.exists():
            raise FileNotFoundError(f"Reference audio not found: {reference_audio}")

        logger.info(f"Cloning voice from: {reference_audio}")
        logger.info(f"Synthesizing: {text[:50]}...")

        # XTTS v2 synthesis with voice cloning
        if output_path:
            self._tts.tts_to_file(
                text=text,
                speaker_wav=str(reference_audio),
                language=language,
                file_path=str(output_path),
            )
            logger.info(f"Saved to: {output_path}")

            # Read back the audio
            return self._read_audio(output_path)
        else:
            # Synthesize to memory
            wav = self._tts.tts(
                text=text,
                speaker_wav=str(reference_audio),
                language=language,
            )
            return np.array(wav, dtype=np.float32)

    def clone_batch(
        self,
        reference_audio: Union[str, Path],
        texts: list,
        language: str = "tr",
        output_dir: Optional[Union[str, Path]] = None,
    ) -> list:
        """
        Clone voice and synthesize multiple texts.

        Args:
            reference_audio: Path to reference audio
            texts: List of texts to synthesize
            language: Language code
            output_dir: Optional directory to save outputs

        Returns:
            List of (text, audio_path) tuples
        """
        self._ensure_loaded()

        results = []
        reference_audio = Path(reference_audio)

        for i, text in enumerate(texts):
            try:
                if output_dir:
                    output_path = Path(output_dir) / f"cloned_{i:03d}.wav"
                    audio = self.clone(reference_audio, text, language, output_path)
                    results.append((text, str(output_path)))
                else:
                    audio = self.clone(reference_audio, text, language)
                    results.append((text, audio))

                logger.info(f"Completed {i+1}/{len(texts)}")

            except Exception as e:
                logger.error(f"Failed to synthesize text {i+1}: {e}")
                results.append((text, None))

        return results

    @staticmethod
    def _read_audio(path: Union[str, Path]) -> np.ndarray:
        """Read audio file to numpy array."""
        import soundfile as sf
        audio, sr = sf.read(str(path))
        return audio.astype(np.float32)

    @staticmethod
    def validate_reference_audio(path: Union[str, Path]) -> dict:
        """
        Validate reference audio for voice cloning.

        Returns:
            Dictionary with validation results
        """
        path = Path(path)

        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'info': {},
        }

        if not path.exists():
            result['errors'].append(f"File not found: {path}")
            return result

        try:
            import soundfile as sf
            audio, sr = sf.read(str(path))

            duration = len(audio) / sr
            result['info']['duration'] = duration
            result['info']['sample_rate'] = sr
            result['info']['samples'] = len(audio)

            # Check duration (minimum 6 seconds recommended)
            if duration < 3:
                result['errors'].append(
                    f"Audio too short: {duration:.1f}s (minimum 6s recommended)"
                )
            elif duration < 6:
                result['warnings'].append(
                    f"Audio is short: {duration:.1f}s (6-30s recommended for best quality)"
                )

            # Check sample rate
            if sr < 16000:
                result['errors'].append(
                    f"Sample rate too low: {sr}Hz (minimum 16kHz recommended)"
                )
            elif sr != 22050 and sr != 24000 and sr != 16000:
                result['warnings'].append(
                    f"Unusual sample rate: {sr}Hz (22050 or 24000 recommended)"
                )

            # Check for silence
            rms = np.sqrt(np.mean(audio ** 2))
            if rms < 0.01:
                result['errors'].append("Audio appears to be silent or very quiet")
            elif rms < 0.05:
                result['warnings'].append("Audio is quite quiet, may affect quality")

            result['valid'] = len(result['errors']) == 0

        except Exception as e:
            result['errors'].append(f"Failed to read audio: {e}")

        return result


def demo():
    """Demonstrate voice cloning."""
    print("Voice Cloning Demo")
    print("=" * 60)

    cloner = VoiceCloner()

    # Check if Coqui TTS is installed
    try:
        cloner.load()
        print("✓ Coqui XTTS v2 loaded successfully")
    except ImportError as e:
        print(f"✗ Coqui TTS not installed: {e}")
        print("\nTo enable voice cloning, run:")
        print("  pip install coqui-tts")
        return

    print("\nVoice cloning requires:")
    print("  - 6+ seconds of clear reference audio")
    print("  - WAV or MP3 format")
    print("  - Single speaker (no background noise)")
    print("\nExample usage:")
    print('  cloner.clone("reference.wav", "Merhaba dünya!")')


if __name__ == "__main__":
    demo()
