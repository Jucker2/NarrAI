from django.test import TestCase
from pathlib import Path

from core.domaine.document import Document
from core.services.narration_pipeline import NarrationPipeline

class NarrationPipelineTests(TestCase):
   def test_pipeline(self):
    

    pdf_path = (
        Path(__file__).parent
        / "files"
        / "test.pdf"
    )

    document = Document(
        title="test",
        pdf_path=str(pdf_path)
    )

    pipeline = NarrationPipeline()

    document = pipeline.process(document)

    # Texte
    self.assertGreater(
        len(document.raw_text),
        0
    )

    self.assertGreater(
        len(document.clean_text),
        0
    )

    # Chapitres
    self.assertGreater(
        len(document.chapters),
        0
    )

    audio_dir = (
        pipeline.storage.root
        / document.uuid
        / "audio"
    )

    # Dossier audio
    self.assertTrue(
        audio_dir.exists()
    )

    # Vérification des chapitres
    for chapter_index, chapter in enumerate(
        document.chapters,
        start=1
    ):

        self.assertGreater(
            len(chapter.chunks),
            0
        )

        chapter_audio_dir = (
            audio_dir
            / f"chapter_{chapter_index:02d}"
        )

        self.assertTrue(
            chapter_audio_dir.exists()
        )

        # WAV des chunks
        chunk_audio_files = sorted(
            chapter_audio_dir.glob("chunk_*.wav")
        )

        self.assertEqual(
            len(chunk_audio_files),
            len(chapter.chunks)
        )

        for audio_file in chunk_audio_files:

            self.assertGreater(
                audio_file.stat().st_size,
                0
            )

        # WAV du chapitre
        chapter_audio = (
            audio_dir
            / f"chapter_{chapter_index:02d}.wav"
        )

        self.assertTrue(
            chapter_audio.exists()
        )

        self.assertGreater(
            chapter_audio.stat().st_size,
            0
        )

    # Audiobook final
    audiobook = (
        audio_dir
        / "audiobook.wav"
    )

    self.assertTrue(
        audiobook.exists()
    )

    self.assertGreater(
        audiobook.stat().st_size,
        0
    )
