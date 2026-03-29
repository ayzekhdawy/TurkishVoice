"""
TurkishVoice CLI - Command Line Interface

Usage:
    turkishvoice synthesize "Merhaba" -o output.wav
    turkishvoice download dfki
    turkishvoice voices --list
    turkishvoice serve
"""

import click
import sys
from pathlib import Path

from turkishvoice import TurkishVoiceEngine, __version__
from turkishvoice.utils.model_downloader import download_voice, list_available_voices, list_downloaded_voices
from turkishvoice.utils.model_downloader import (
    download_voice,
    list_available_voices,
    list_downloaded_voices,
)


@click.group()
@click.version_option(version=__version__)
def cli():
    """
    TurkishVoice - Açık Kaynak Türkçe Metin-Şarkı Sentezi

    Python kütüphanesi, CLI ve Web API ile kullanılabilir.

    Örnekler:

        turkishvoice download dfki

        turkishvoice synthesize "Günaydın" -o output.wav

        turkishvoice voices --list

        turkishvoice serve
    """
    pass


@cli.command()
@click.argument('voice', required=False, default='dfki')
@click.option('--force', is_flag=True, help='Force re-download')
def download(voice, force):
    """
    Türkçe Piper TTS ses modelini indir.

    Mevcut sesler: dfki, fahrettin, fettah

    Örnekler:

        turkishvoice download dfki

        turkishvoice download fahrettin

        turkishvoice download --force dfki
    """
    click.echo(f"Downloading voice: {voice}")
    result = download_voice(voice, force=force)
    if result:
        click.echo(f"✓ Voice '{voice}' downloaded successfully!")
        click.echo(f"  Path: {result}")
    else:
        click.echo(f"✗ Failed to download voice '{voice}'", err=True)
        sys.exit(1)


@cli.command()
@click.option('--list', 'list_voices', is_flag=True, help='List available voices')
@click.option('--show', 'show_downloaded', is_flag=True, help='Show downloaded voices')
def voices(list_voices, show_downloaded):
    """
    Türkçe seslerini yönet ve listele.

    Örnekler:

        turkishvoice voices --list

        turkishvoice voices --show
    """
    if list_voices:
        list_available_voices()
    elif show_downloaded:
        downloaded = list_downloaded_voices()
        if downloaded:
            click.echo("\nDownloaded voices:")
            for v in downloaded:
                click.echo(f"  {v['name']}: {v['path']}")
        else:
            click.echo("No voices downloaded yet. Run 'turkishvoice download dfki' first.")
    else:
        # Default: show both
        click.echo("\n=== Available Voices ===")
        list_available_voices()
        click.echo("\n=== Downloaded Voices ===")
        downloaded = list_downloaded_voices()
        if downloaded:
            for v in downloaded:
                click.echo(f"  ✓ {v['name']}: {v['path']}")
        else:
            click.echo("  No voices downloaded yet.")


@cli.command()
@click.argument('text')
@click.option(
    '-o', '--output',
    'output_path',
    help='Çıktı dosya yolu (varsayılan: output.wav)',
)
@click.option(
    '-v', '--voice',
    default='dfki',
    help='Kullanılacak ses (varsayılan: dfki)',
)
@click.option(
    '--speed',
    default=1.0,
    type=float,
    help='Konuşma hızı 0.5-2.0 (varsayılan: 1.0)',
)
@click.option(
    '--pitch',
    default=1.0,
    type=float,
    help='Perde çarpanı 0.5-2.0 (varsayılan: 1.0)',
)
@click.option(
    '--format',
    'audio_format',
    default='wav',
    type=click.Choice(['wav', 'mp3', 'ogg']),
    help='Ses formatı (varsayılan: wav)',
)
@click.option(
    '--list-voices',
    is_flag=True,
    help='List available voices and exit',
)
def synthesize(text, output_path, voice, speed, pitch, audio_format, list_voices):
    """
    Türkçe metni sese dönüştür.

    Örnekler:

        turkishvoice synthesize "Merhaba dünya"

        turkishvoice synthesize "Günaydın" -o selam.wav --voice emel

        turkishvoice synthesize "Çok güzel!" --speed 0.8 --pitch 1.2
    """
    if list_voices:
        list_available_voices()
        return

    try:
        # Initialize engine with Edge TTS (online, high quality)
        click.echo(f"Edge TTS başlatılıyor: {voice}")
        engine = TurkishVoiceEngine(voice=voice, use_edge=True, use_piper=False)

        # Validate parameters
        if not 0.5 <= speed <= 2.0:
            click.echo("Hata: Hız 0.5 ile 2.0 arasında olmalı.", err=True)
            sys.exit(1)

        if not 0.5 <= pitch <= 2.0:
            click.echo("Hata: Perde 0.5 ile 2.0 arasında olmalı.", err=True)
            sys.exit(1)

        # Synthesize
        click.echo(f"Sentezleniyor: {text[:50]}{'...' if len(text) > 50 else ''}")
        audio = engine.synthesize(
            text=text,
            speed=speed,
            pitch=pitch,
        )

        # Determine output path
        if output_path is None:
            output_path = 'output.wav'

        # Save audio
        engine.save(audio, output_path, format=audio_format)

        # Show duration
        duration = len(audio) / engine.sample_rate
        click.echo(f"Kaydedildi: {output_path} ({duration:.2f}s)")

    except FileNotFoundError as e:
        click.echo(f"Hata: Model bulunamadı.", err=True)
        click.echo("Run 'turkishvoice download dfki' first.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Hata: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    '-o', '--output-dir',
    'output_dir',
    default='output',
    help='Çıktı dizini (varsayılan: output)',
)
@click.option(
    '-v', '--voice',
    default='dfki',
    help='Kullanılacak ses (varsayılan: dfki)',
)
@click.option(
    '--parallel',
    default=4,
    type=int,
    help='Paralel işlem sayısı (varsayılan: 4)',
)
@click.argument('input_file', type=click.Path(exists=True))
def batch(input_file, output_dir, voice, parallel):
    """
    Dosyadan toplu sentez işlemi yap.

    INPUT_FILE: Her satırında bir cümle olan metin dosyası

    Örnek:

        turkishvoice batch sentences.txt -o output/ --voice fahrettin
    """
    from tqdm import tqdm

    input_path = Path(input_file)
    output_path = Path(output_dir)

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Read sentences
    click.echo(f"Dosya okunuyor: {input_file}")
    sentences = input_path.read_text(encoding='utf-8').splitlines()
    sentences = [s.strip() for s in sentences if s.strip()]
    total = len(sentences)

    click.echo(f"{total} cümle bulundu.")
    click.echo(f"Çıktı dizini: {output_path}")
    click.echo(f"Kullanılan ses: {voice}")

    # Initialize engine
    engine = TurkishVoiceEngine(voice=voice, use_piper=True)

    # Process sentences
    click.echo("\nİşleniyor...")

    for i, sentence in enumerate(tqdm(sentences, desc="Sentezleniyor")):
        output_file = output_path / f"output_{i:05d}.wav"

        try:
            audio = engine.synthesize(sentence, voice=voice)
            engine.save(audio, str(output_file))
        except Exception as e:
            tqdm.write(f"Hata [{i}]: {e}")

    click.echo(f"\nTamamlandı! {total} dosya {output_path} dizinine kaydedildi.")


@cli.command()
@click.option(
    '--host',
    default='0.0.0.0',
    help='Sunucu adresi (varsayılan: 0.0.0.0)',
)
@click.option(
    '-p', '--port',
    default=7860,
    type=int,
    help='Port numarası (varsayılan: 7860)',
)
@click.option(
    '--api',
    is_flag=True,
    help='Sadece API modu (Web UI olmadan)',
)
def serve(host, port, api):
    """
    TurkishVoice Web UI veya API sunucu başlat.

    Örnekler:

        turkishvoice serve

        turkishvoice serve --port 8080

        turkishvoice serve --api
    """
    import uvicorn

    if api:
        # Start API-only server
        click.echo(f"API sunucusu başlatılıyor: http://{host}:{port}")
        click.echo("API endpoint: /api/v1/synthesize")
        uvicorn.run(
            "turkishvoice.api.main:app",
            host=host,
            port=port,
            reload=False,
        )
    else:
        # Start Web UI server
        click.echo(f"Web UI sunucusu başlatılıyor: http://{host}:{port}")
        click.echo("(Ctrl+C ile durdur)")

        try:
            from turkishvoice.webui.app import create_app
            app = create_app()
            app.launch(server_name=host, server_port=port, inbrowser=True)
        except ImportError as e:
            click.echo(f"Web UI başlatılamadı: {e}", err=True)
            click.echo("Gradio kurulu değil. pip install turkishvoice[webui] deneyin.")
            sys.exit(1)


@cli.command()
@click.argument('voice_name', required=False, default='dfki')
@click.option('--force', '-f', is_flag=True, help='Force re-download')
def download(voice_name, force):
    """
    Piper TTS Türkçe ses modelini indir.

    Mevcut sesler: dfki, fahrettin, fettah

    Örnek:

        turkishvoice download dfki

        turkishvoice download fahrettin --force
    """
    click.echo(f"Downloading voice: {voice_name}")
    result = download_voice(voice_name, force=force)
    if result:
        click.echo(f"Voice downloaded to: {result}")
    else:
        click.echo("Download failed!", err=True)
        sys.exit(1)


@cli.command()
def voices():
    """
    Mevcut ve indirilmiş sesleri listele.

    Örnek:

        turkishvoice voices
    """
    click.echo("\n=== Available Piper Voices ===")
    list_available_voices()

    click.echo("\n=== Downloaded Voices ===")
    downloaded = list_downloaded_voices()
    if downloaded:
        for v in downloaded:
            click.echo(f"  [OK] {v['name']}: {v['path']}")
    else:
        click.echo("  No voices downloaded yet.")
        click.echo("\n  Run 'turkishvoice download dfki' to download a voice.")


@cli.command()
@click.option('--voice', '-v', default=None, help='İndirilecek ses (dfki, fahrettin, fettah)')
@click.option('--list', '-l', 'list_voices', is_flag=True, help='Mevcut sesleri listele')
@click.option('--show', '-s', 'show_downloaded', is_flag=True, help='İndirilen sesleri göster')
def download(voice, list_voices, show_downloaded):
    """
    Piper TTS Türkçe ses modellerini indir.

    Örnekler:

        turkishvoice download --voice dfki

        turkishvoice download --list

        turkishvoice download --show
    """
    if list_voices:
        list_available_voices()
        return

    if show_downloaded:
        downloaded = list_downloaded_voices()
        if downloaded:
            click.echo("\nİndirilen sesler:")
            for v in downloaded:
                click.echo(f"  {v['name']}: {v['path']}")
        else:
            click.echo("\nHenüz indirilen ses yok.")
            click.echo("  'turkishvoice download --voice dfki' ile indirebilirsiniz.")
        return

    if voice:
        click.echo(f"Ses indiriliyor: {voice}")
        result = download_voice(voice)
        if result:
            click.echo(f"\nBaşarıyla indirildi: {result}")
        else:
            click.echo("İndirme başarısız oldu.", err=True)
            sys.exit(1)
    else:
        click.echo("Kullanım: turkishvoice download --voice dfki")
        click.echo("\nMevcut sesler:")
        list_available_voices()


@cli.command()
def info():
    """
    TurkishVoice motor bilgilerini göster.
    """
    engine = TurkishVoiceEngine(voice='dfki', use_piper=True)
    engine_info = engine.get_engine_info()

    click.echo("\nTurkishVoice Motor Bilgileri")
    click.echo("-" * 40)
    for key, value in engine_info.items():
        click.echo(f"  {key}: {value}")
    click.echo()


@cli.command()
@click.argument('reference_audio', type=click.Path(exists=True))
@click.option(
    '--text',
    '-t',
    required=True,
    help='Sentezlenecek metin',
)
@click.option(
    '-o', '--output',
    'output_path',
    default='cloned_output.wav',
    help='Çıktı dosya yolu',
)
@click.option(
    '--validate',
    is_flag=True,
    help='Referans sesi doğrula ve çık',
)
def clone(reference_audio, text, output_path, validate):
    """
    Ses klonlama ile sentez yap (Coqui XTTS).

    Referans ses dosyasından speaker embedding çıkararak
    o sese benzer sentez yapar.

    Örnekler:

        turkishvoice clone ref.wav -t "Merhaba dünya" -o output.wav

        turkishvoice clone ref.wav --validate  # Sadece doğrula

    Not: Coqui TTS kurulumu gerekir: pip install turkishvoice[clone]
    """
    from turkishvoice.core.voice_cloner import VoiceCloner

    # Validate audio first
    cloner = VoiceCloner()
    validation = cloner.validate_reference_audio(reference_audio)

    click.echo(f"Referans ses: {reference_audio}")
    if validation['info'].get('duration'):
        click.echo(f"Süre: {validation['info']['duration']:.1f}s")

    if validate:
        if validation['valid']:
            click.echo("✓ Referans ses geçerli")
        else:
            click.echo("✗ Referans ses geçersiz")
            for err in validation['errors']:
                click.echo(f"  Hata: {err}")
        return

    if not validation['valid']:
        click.echo("✗ Referans ses hatalı:", err=True)
        for err in validation['errors']:
            click.echo(f"  {err}")
        sys.exit(1)

    for warn in validation.get('warnings', []):
        click.echo(f"  Uyarı: {warn}")

    # Clone voice
    try:
        click.echo("Ses klonlanıyor...")
        audio = cloner.clone(reference_audio, text, language='tr')

        # Save output
        cloner._tts.tts_to_file(
            text=text,
            speaker_wav=str(reference_audio),
            language='tr',
            file_path=str(output_path),
        )

        click.echo(f"✓ Klonlanmış ses kaydedildi: {output_path}")

    except ImportError:
        click.echo("✗ Coqui TTS kurulu değil", err=True)
        click.echo("Kurulum: pip install turkishvoice[clone]", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"✗ Hata: {e}", err=True)
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
