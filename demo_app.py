"""
TurkishVoice Demo App for Hugging Face Spaces

Run locally:
    pip install gradio edge-tts
    python demo_app.py

Deploy to Hugging Face Spaces:
    1. Create new Space at https://huggingface.co/spaces
    2. Select Gradio SDK
    3. Upload this file + requirements.txt
"""

import gradio as gr
from pathlib import Path
import tempfile

# Use Edge TTS for demo (no model download required)
from turkishvoice.core.piper_engine import EdgeTTSVoice

# Global engine
_engine = None


def get_engine():
    """Get Edge TTS engine."""
    global _engine
    if _engine is None:
        _engine = EdgeTTSVoice(voice='emel')
    return _engine


def synthesize_turkish(text: str, voice: str, speed: float):
    """
    Synthesize Turkish text to speech.

    Args:
        text: Turkish text input
        voice: Voice selection (emel or ahmet)
        speed: Speech speed (0.5-2.0)

    Returns:
        Tuple of (audio_file, status_message)
    """
    if not text or not text.strip():
        return None, "❌ Lütfen Türkçe metin girin."

    if len(text) > 5000:
        return None, "❌ Metin çok uzun (max 5000 karakter)."

    try:
        engine = get_engine()

        # Switch voice if needed
        if voice != engine.voice_name:
            engine = EdgeTTSVoice(voice=voice)

        # Synthesize
        audio = engine.synthesize(text, speed=speed)

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            output_path = f.name

        # Write WAV file
        import soundfile as sf
        sf.write(output_path, audio, 24000)

        duration = len(audio) / 24000
        status = f"✅ Başarılı! ({duration:.2f} saniye)"

        return output_path, status

    except Exception as e:
        return None, f"❌ Hata: {str(e)}"


def create_demo():
    """Create Gradio demo interface."""

    with gr.Blocks(
        title="TurkishVoice Demo",
        theme=gr.themes.Soft(),
        css="""
        .container { max-width: 800px; margin: auto; }
        .header { text-align: center; margin-bottom: 20px; }
        .footer { text-align: center; margin-top: 30px; color: #666; }
        """,
    ) as demo:

        gr.Markdown("""
        # 🇹🇷 TurkishVoice - Türkçe Metin Okuma

        **Açık kaynaklı Türkçe Text-to-Speech sistemi**

        - 🚀 Gerçek zamanlı ses sentezi
        - 🎯 Microsoft Azure neural kalitesi
        - 🔓 Tamamen açık kaynak

        [GitHub](https://github.com/ayzekhdawy/TurkishVoice) |
        [Dokümantasyon](https://github.com/ayzekhdawy/TurkishVoice#readme)
        """)

        with gr.Row():
            with gr.Column(scale=2):
                text_input = gr.Textbox(
                    label="Türkçe Metin",
                    placeholder="Buraya sentezlemek istediğiniz metni yazın...\n\nÖrnek: 'Merhaba dünya! TurkishVoice ile tanışın.'",
                    lines=5,
                    max_lines=10,
                )

                with gr.Row():
                    voice_dropdown = gr.Dropdown(
                        choices=[
                            ("Emel (Kadın)", "emel"),
                            ("Ahmet (Erkek)", "ahmet"),
                        ],
                        value="emel",
                        label="Ses",
                    )

                    speed_slider = gr.Slider(
                        minimum=0.5,
                        maximum=2.0,
                        value=1.0,
                        step=0.1,
                        label="Hız",
                    )

                synthesize_btn = gr.Button(
                    "🔊 Sentezle",
                    variant="primary",
                    size="lg",
                )

            with gr.Column(scale=1):
                audio_output = gr.Audio(
                    label="Ses Çıktısı",
                    type="filepath",
                )
                status_output = gr.Textbox(
                    label="Durum",
                    interactive=False,
                    lines=2,
                )

        # Examples
        gr.Markdown("### 📝 Örnek Cümleler")
        gr.Examples(
            examples=[
                ["Merhaba dünya! TurkishVoice ile tanışın."],
                ["Türkçe metin okuma sistemi başarıyla çalışıyor."],
                ["Yapay zeka teknolojileri hızla gelişmeye devam ediyor."],
                ["Bu bir demo uygulamasıdır. Ses kalitesini test edebilirsiniz."],
                ["Görme engelliler için metinleri sese dönüştürebilirsiniz."],
            ],
            inputs=[text_input],
        )

        # Features
        gr.Markdown("""
        ### ✨ Özellikler

        | Özellik | Açıklama |
        |---------|----------|
        | 🎙️ Neural TTS | Microsoft Azure altyapısı |
        | ⚡ Gerçek Zamanlı | ~1 saniye gecikme |
        | 🇹🇷 Türkçe Özel | Türkçe dil desteği |
        | 🔊 İki Ses | Kadın (Emel) ve Erkek (Ahmet) |
        | 🎛️ Hız Kontrolü | 0.5x - 2.0x arası |
        """)

        # Footer
        gr.Markdown("""
        ---
        **TurkishVoice** v0.2.0 | Apache 2.0 Lisans

        Made with ❤️ for the Turkish community
        """)

        # Event handlers
        synthesize_btn.click(
            fn=synthesize_turkish,
            inputs=[text_input, voice_dropdown, speed_slider],
            outputs=[audio_output, status_output],
        )

    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )
