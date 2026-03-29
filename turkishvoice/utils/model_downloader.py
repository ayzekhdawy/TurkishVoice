"""
TurkishVoice Model Downloader

Downloads Piper TTS models from HuggingFace.
"""

import os
import hashlib
import shutil
from pathlib import Path
from typing import Optional, Dict
import urllib.request
import urllib.error

# Piper Turkish voice models
# Note: fahrettin and fettah were removed from main repo at contributor request
# Only dfki is officially available
TURKISH_VOICES: Dict[str, Dict] = {
    'dfki': {
        'model': 'tr_TR-dfki-medium.onnx',
        'config': 'tr_TR-dfki-medium.onnx.json',
        'size': '63 MB',
        'quality': 'medium',
        'hf_path': 'tr/tr_TR/dfki/medium',  # HuggingFace path
    },
}

# Alternative Turkish voices (if available in community repos)
ALT_TURKISH_VOICES: Dict[str, Dict] = {
    'fahrettin': {
        'model': 'tr_TR-fahrettin-medium.onnx',
        'config': 'tr_TR-fahrettin-medium.onnx.json',
        'size': '67 MB',
        'quality': 'medium',
    },
    'fettah': {
        'model': 'tr_TR-fettah-medium.onnx',
        'config': 'tr_TR-fettah-medium.onnx.json',
        'size': '65 MB',
        'quality': 'medium',
    },
}

# HuggingFace URLs for Piper voices
# Main repo: https://huggingface.co/rhasspy/piper-voices/tree/main/tr
HF_VOICES_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

# GitHub releases (fallback)
GITHUB_BASE_URL = "https://github.com/rhasspy/piper-voices/releases/download/v1.0.0"


def get_model_dir() -> Path:
    """Get the model directory path."""
    # Use user's home directory
    home = Path.home()
    model_dir = home / ".turkishvoice" / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    return model_dir


def get_cache_dir() -> Path:
    """Get the cache directory for temporary files."""
    home = Path.home()
    cache_dir = home / ".turkishvoice" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def download_file(url: str, dest_path: Path, description: str = "File") -> bool:
    """
    Download a file from URL with progress.

    Args:
        url: Source URL
        dest_path: Destination file path
        description: Description for progress display

    Returns:
        True if successful, False otherwise
    """
    print(f"Downloading {description} from {url}...")

    try:
        # Add user agent to avoid some download blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=300) as response:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            downloaded = 0

            with open(dest_path, 'wb') as f:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break

                    f.write(buffer)
                    downloaded += len(buffer)

                    # Show progress
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r  Progress: {percent:.1f}%", end='', flush=True)

            print()  # New line after progress
            return True

    except urllib.error.URLError as e:
        print(f"Error downloading {description}: {e}")
        if dest_path.exists():
            dest_path.unlink()
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        if dest_path.exists():
            dest_path.unlink()
        return False


def download_voice(voice_name: str, force: bool = False) -> Optional[Path]:
    """
    Download a Turkish Piper voice model.

    Args:
        voice_name: Voice identifier ('dfki', 'fahrettin', 'fettah')
        force: Force re-download even if exists

    Returns:
        Path to model file, or None if failed
    """
    if voice_name not in TURKISH_VOICES:
        print(f"Error: Unknown voice '{voice_name}'")
        print(f"Available voices: {', '.join(TURKISH_VOICES.keys())}")
        return None

    voice_info = TURKISH_VOICES[voice_name]
    model_dir = get_model_dir()

    model_path = model_dir / voice_info['model']
    config_path = model_dir / voice_info['config']

    # Check if already exists
    if model_path.exists() and config_path.exists() and not force:
        print(f"Voice '{voice_name}' already exists at {model_path}")
        return model_path

    # Download model - try multiple URLs with correct HuggingFace structure
    # Path: tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx
    hf_path = voice_info.get('hf_path', f'tr/tr_TR/{voice_name}/medium')

    urls_to_try = [
        f"{HF_VOICES_BASE}/{hf_path}/{voice_info['model']}",
        f"{HF_VOICES_BASE}/tr/tr_TR/{voice_name}/medium/{voice_info['model']}",
        f"{GITHUB_BASE_URL}/{voice_info['model']}",  # GitHub fallback
    ]

    model_downloaded = False
    for i, model_url in enumerate(urls_to_try):
        suffix = "" if i == 0 else f" (mirror {i})"
        if download_file(model_url, model_path, f"Model ({voice_info['size']}){suffix}"):
            model_downloaded = True
            break

    if not model_downloaded:
        print("Error: Could not download model from any source")
        print("Try downloading manually from: https://huggingface.co/rhasspy/piper-voices/tree/main/tr")
        return None

    # Download config
    config_url = f"{HF_VOICES_BASE}/{hf_path}/{voice_info['config']}"
    if not download_file(config_url, config_path, "Config"):
        print("Warning: Config download failed, but model may still work")

    print(f"Successfully downloaded '{voice_name}' voice!")
    print(f"  Model: {model_path}")
    print(f"  Config: {config_path}")

    return model_path


def list_available_voices() -> None:
    """List all available Turkish voices."""
    print("\nAvailable Turkish Piper Voices:")
    print("-" * 50)

    for name, info in TURKISH_VOICES.items():
        print(f"  {name:12} - {info['quality']:8} quality ({info['size']})")

    print("-" * 50)
    print(f"\nModel directory: {get_model_dir()}")


def list_downloaded_voices() -> list:
    """List downloaded voices."""
    model_dir = get_model_dir()
    downloaded = []

    for voice_name, info in TURKISH_VOICES.items():
        model_path = model_dir / info['model']
        if model_path.exists():
            downloaded.append({
                'name': voice_name,
                'path': str(model_path),
                'config': str(model_dir / info['config']),
            })

    return downloaded


def get_voice_path(voice_name: str) -> Optional[Path]:
    """
    Get path to a voice model, downloading if necessary.

    Args:
        voice_name: Voice identifier

    Returns:
        Path to model file, or None if not available
    """
    if voice_name not in TURKISH_VOICES:
        return None

    model_dir = get_model_dir()
    model_path = model_dir / TURKISH_VOICES[voice_name]['model']

    if not model_path.exists():
        return download_voice(voice_name)

    return model_path


def main():
    """CLI for model downloader."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m turkishvoice.utils.model_downloader [command] [voice]")
        print("\nCommands:")
        print("  list          - List available voices")
        print("  download NAME - Download a voice (dfki, fahrettin, fettah)")
        print("  show          - Show downloaded voices")
        return

    command = sys.argv[1]

    if command == 'list':
        list_available_voices()
    elif command == 'download':
        if len(sys.argv) < 3:
            print("Error: Please specify voice name")
            print(f"Available: {', '.join(TURKISH_VOICES.keys())}")
            return
        voice_name = sys.argv[2]
        download_voice(voice_name)
    elif command == 'show':
        downloaded = list_downloaded_voices()
        if downloaded:
            print("\nDownloaded voices:")
            for v in downloaded:
                print(f"  {v['name']}: {v['path']}")
        else:
            print("No voices downloaded yet.")
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
