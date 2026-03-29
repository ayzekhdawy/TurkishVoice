"""
TurkishVoice Gradio Web UI

A web-based interface for Turkish Text-to-Speech synthesis.
"""

import gradio as gr
import numpy as np
from pathlib import Path
import tempfile
import os

from turkishvoice import TurkishVoiceEngine, __version__


# Global engine instance
_engine = None


def get_engine() -> TurkishVoiceEngine:
    """Get or create the global engine instance."""
    global _engine
    if _engine is None:
        _engine = TurkishVoiceEngine()
    return _engine


def synthesize_speech(
    text: str,
    voice: str,
    speed: float,
    pitch: float,
    prosody: float,
) -> tuple:
    """
    Synthesize speech from text.

    Args:
        text: Turkish text to synthesize
        voice: Voice identifier
        speed: Speech speed (0.5-2.0)
        pitch: Pitch multiplier (0.5-2.0)
        prosody: Prosody scale (0.0-2.0)

    Returns:
        Tuple of (audio_output, status_text)
    """
    if not text or not text.strip():
        return None, "Lütfen metin girin."

    try:
        engine = get_engine()

        # Synthesize
        audio = engine.synthesize(
            text=text,
            voice=voice,
            speed=speed,
            pitch=pitch,
            prosody_scale=prosody,
        )

        # Save to temp file
        temp_dir = Path(tempfile.gettempdir()) / "turkishvoice"
        temp_dir.mkdir(exist_ok=True)
        temp_file = temp_dir / f"gradio_output_{os.getpid()}.wav"

        engine.save(audio, str(temp_file))

        duration = len(audio) / engine.sample_rate
        status = f"✓ Sentez tamamlandı! ({duration:.2f} saniye)"

        return str(temp_file), status

    except Exception as e:
        return None, f"Hata: {str(e)}"


def list_available_voices() -> list:
    """Get list of available voices for dropdown."""
    engine = get_engine()
    voices = engine.get_available_voices()
    return [(f"{v['name']} ({v['gender']})", v['id']) for v in voices]


def get_voice_preview(voice_id: str) -> tuple:
    """Generate a preview for a voice."""
    try:
        engine = get_engine()
        text = "Merhaba, ben TurkishVoice! Türkçe metinleri sese dönüştürüyorum."
        audio = engine.synthesize(text=text, voice=voice_id)

        temp_dir = Path(tempfile.gettempdir()) / "turkishvoice"
        temp_dir.mkdir(exist_ok=True)
        temp_file = temp_dir / f"preview_{voice_id}.wav"

        engine.save(audio, str(temp_file))
        return str(temp_file), f"✓ {voice_id} sesi önizlemesi"

    except Exception as e:
        return None, f"Hata: {str(e)}"


def clone_voice_reference(
    reference_audio: str,
    voice_name: str,
) -> tuple:
    """
    Clone a voice from reference audio.

    Note: This is a placeholder. Real implementation requires
    speaker embedding extraction and model fine-tuning.
    """
    if reference_audio is None:
        return None, "Lütfen referans ses dosyası yükleyin."

    if not voice_name or not voice_name.strip():
        return None, "Lütfen ses için bir isim girin."

    # Placeholder response
    return None, "Ses klonlama yakında aktif olacak. Şu an için varsayılan sesleri kullanabilirsiniz."


def create_app() -> gr.Blocks:
    """
    Create the Gradio application.

    Returns:
        Gradio Blocks application
    """

    # CSS styling with Turkish flag colors
    css = """
    .turkishvoice-header {
        background: linear-gradient(135deg, #E30A17 0%, #FF0000 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .turkishvoice-header h1 {
        color: white;
        font-size: 2em;
        margin: 0;
    }
    .turkishvoice-header p {
        color: rgba(255,255,255,0.9);
        margin: 10px 0 0 0;
    }
    .voice-card {
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        background: #fafafa;
    }
    .status-box {
        padding: 10px;
        border-radius: 5px;
        background: #f0f0f0;
        text-align: center;
    }
    .success {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 0.9em;
    }
    """

    with gr.Blocks(css=css, title="TurkishVoice - Türkçe TTS") as app:

        # Header
        gr.HTML("""
        <div class="turkishvoice-header">
            <h1>🇹🇷 TurkishVoice</h1>
            <p>Açık Kaynak Türkçe Metin-Şarkı Sentezi | v""" + __version__ + """</p>
        </div>
        """)

        with gr.Tabs():
            # Tab 1: Text to Speech
            with gr.TabItem("📝 Metin → Ses"):
                with gr.Row():
                    with gr.Column(scale=2):
                        text_input = gr.Textbox(
                            label="Türkçe Metin",
                            placeholder="Buraya sentezlemek istediğiniz Türkçe metni yazın...",
                            lines=5,
                            max_lines=10,
                        )

                        with gr.Row():
                            voice_dropdown = gr.Dropdown(
                                choices=list_available_voices(),
                                value="default",
                                label="Ses Seçimi",
                            )
                            format_dropdown = gr.Dropdown(
                                choices=["WAV", "MP3", "OGG"],
                                value="WAV",
                                label="Format",
                            )

                        with gr.Row():
                            speed_slider = gr.Slider(
                                minimum=0.5,
                                maximum=2.0,
                                value=1.0,
                                step=0.1,
                                label="Hız (0.5 - 2.0)",
                            )
                            pitch_slider = gr.Slider(
                                minimum=0.5,
                                maximum=2.0,
                                value=1.0,
                                step=0.1,
                                label="Perde (0.5 - 2.0)",
                            )
                            prosody_slider = gr.Slider(
                                minimum=0.0,
                                maximum=2.0,
                                value=1.0,
                                step=0.1,
                                label="Doğallık (0.0 - 2.0)",
                            )

                        with gr.Row():
                            synthesize_btn = gr.Button(
                                "🔊 Sentezle",
                                variant="primary",
                                size="lg",
                            )
                            clear_btn = gr.Button(
                                "🗑️ Temizle",
                                variant="secondary",
                            )

                    with gr.Column(scale=1):
                        audio_output = gr.Audio(
                            label="Sonuç",
                            type="filepath",
                        )
                        status_output = gr.Textbox(
                            label="Durum",
                            interactive=False,
                            lines=2,
                        )

                        gr.HTML("""
                        <div class="voice-card">
                            <h4>💡 İpuçları</h4>
                            <ul>
                                <li>Maksimum 5000 karakter kullanabilirsiniz</li>
                                <li>Hız: 0.5 = yavaş, 1.0 = normal, 2.0 = hızlı</li>
                                <li>Perde: 0.5 = kalın, 1.0 = normal, 2.0 = ince</li>
                                <li>Doğallık: 0.0 = robotik, 1.0 = normal, 2.0 = abartılı</li>
                            </ul>
                        </div>
                        """)

            # Tab 2: Voice Cloning
            with gr.TabItem("🎭 Ses Klonlama"):
                gr.Markdown("""
                ## Ses Klonlama
                Kendi sesinizi oluşturmak için 10-30 saniye referans ses yükleyin.

                > ⚠️ **Not:** Ses klonlama özelliği henüz geliştirme aşamasındadır.
                """)
                with gr.Row():
                    with gr.Column():
                        reference_audio = gr.Audio(
                            label="Referans Ses (10-30 saniye)",
                            type="filepath",
                        )
                        voice_name_input = gr.Textbox(
                            label="Ses Adı",
                            placeholder="örn: Ahmet'in sesi",
                        )
                        clone_btn = gr.Button(
                            "🎭 Klonla",
                            variant="primary",
                        )

                    with gr.Column():
                        clone_status = gr.Textbox(
                            label="Durum",
                            interactive=False,
                            lines=3,
                        )

                gr.Markdown("""
                ### Nasıl Çalışır?

                1. **Referans Ses Yükle**: 10-30 saniye arası Türkçe konuşma
                2. **Ses Adı Ver**: Kendi sesinize bir isim verin
                3. **Klonla**: Ses profili oluşturulur
                4. **Kullan**: Oluşturulan sesle metin sentezleyin

                > ⚠️ Sadece kendi sesinizi veya izin aldığınız sesleri kullanabilirsiniz.
                """)

            # Tab 3: Batch Processing
            with gr.TabItem("📦 Toplu İşlem"):
                gr.Markdown("""
                ## Toplu Sentez
                Bir dosyadaki birden fazla metni sırayla sentezleyin.
                """)

                with gr.Row():
                    with gr.Column():
                        batch_file = gr.File(
                            label="Metin Dosyası (her satıra bir cümle)",
                            file_count="single",
                            file_types=[".txt"],
                        )
                        batch_voice = gr.Dropdown(
                            choices=list_available_voices(),
                            value="default",
                            label="Ses Seçimi",
                        )
                        batch_btn = gr.Button(
                            "📦 İşleme Başla",
                            variant="primary",
                        )

                    with gr.Column():
                        batch_output = gr.Textbox(
                            label="İlerleme",
                            interactive=False,
                            lines=5,
                        )

                gr.Markdown("""
                ### Dosya Formatı

                ```
                Merhaba, nasılsın?
                Bugün hava çok güzel.
                TurkishVoice ile Türkçe konuşma sentezleyebilirsiniz.
                ```

                Her satır ayrı bir cümle olarak işlenir.
                """)

            # Tab 4: Settings
            with gr.TabItem("⚙️ Ayarlar"):
                gr.Markdown("""
                ## Ayarlar
                TurkishVoice motorunu yapılandırın.
                """)

                engine = get_engine()
                info = engine.get_engine_info()

                gr.Markdown(f"""
                ### Motor Bilgileri

                | Özellik | Değer |
                |---------|-------|
                | Versiyon | {info['version']} |
                | Örnekleme Hızı | {info['sample_rate']} Hz |
                | Model Tipi | {info['model_type']} |
                | Vocoder | {info['vocoder_type']} |
                | ONNX | {'Evet' if info['use_onnx'] else 'Hayır'} |

                ### Gelişmiş Ayarlar

                *(Yakında eklenecek)*

                - Model seçimi
                - Özel ses yükleme
                - Eğitim parametreleri
                """)

        # Footer
        gr.HTML("""
        <div class="footer">
            <p>TurkishVoice - Açık Kaynak Türkçe TTS | Apache 2.0 Lisans</p>
            <p>
                <a href="https://github.com/turkishvoice/turkishvoice">GitHub</a> |
                <a href="https://turkishvoice.ai/docs">Dokümantasyon</a> |
                <a href="https://discord.gg/turkishvoice">Discord</a>
            </p>
        </div>
        """)

        # Event handlers
        synthesize_btn.click(
            fn=synthesize_speech,
            inputs=[text_input, voice_dropdown, speed_slider, pitch_slider, prosody_slider],
            outputs=[audio_output, status_output],
        )

        clear_btn.click(
            fn=lambda: (None, ""),
            outputs=[text_input, status_output],
        )

        clone_btn.click(
            fn=clone_voice_reference,
            inputs=[reference_audio, voice_name_input],
            outputs=[reference_audio, clone_status],
        )

        batch_btn.click(
            fn=lambda f, v: f"Toplu işlem yakında aktif olacak. Dosya: {f}",
            inputs=[batch_file, batch_voice],
            outputs=[batch_output],
        )

    return app


def main():
    """Launch the Gradio app."""
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
    )


if __name__ == "__main__":
    main()
