from django.test import TestCase
from pathlib import Path

from core.domaine.document import Document
from core.services.narration_pipeline import NarrationPipeline

class NarrationPipelineTests(TestCase):
    def test_pipeline(self):
        pdf_path=(Path(__file__).parent / "files" / "test.pdf")
        document=Document(title="test",pdf_path=str(pdf_path))
        pipeline=NarrationPipeline()

        document=pipeline.process(document)

        self.assertGreater(len(document.raw_text),0)  
        self.assertGreater(len(document.clean_text),0)
        self.assertGreater(len(document.chapters),0)

        storage_dir= (
            Path("storage") / document.uuid
        )

        chunks_dir=storage_dir / "chunks"
        audio_dir= storage_dir / "audio"

        self.assertTrue(chunks_dir.exists())
        self.assertTrue(audio_dir.exists())

        for chapter_index,chapter in enumerate(document.chapters,start=1):
            chapter_chunks_dir=(
                chunks_dir / f"chapter_{chapter_index:02d}"
            )

            chapter_audio_dir=(
                audio_dir / f"chapter_{chapter_index:02d}"
            )

            self.assertTrue(
                chapter_chunks_dir.exists()
            )
            self.assertTrue(
                chapter_audio_dir.exists()
            )

            self.assertGreater(
                len(chapter.chunks),0
            )

            for chunk in chapter.chunks:
                chunk_text=(
                    chapter_chunks_dir / f"chunk_{chunk.index:04d}.txt"
                )

                chunk_audio=(
                    chapter_audio_dir / f"chunk_{chunk.index:04d}.wav"
                )

                self.assertTrue(chunk_text.exists())
                self.assertTrue(chunk_audio.exists())

                self.assertGreater(
                    chunk_audio.stat().st_size,0
                )

