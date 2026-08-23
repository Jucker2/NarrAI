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