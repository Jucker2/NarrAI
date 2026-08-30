from core.domaine.document import Document

from core.services.pdf_extractor import PDFExtractor
from core.services.text_cleaner import TextCleaner
from core.services.text_preprocessor import TextPreprocessor
from core.services.chapter_detector import ChapterDetector
from core.services.text_chunker import TextChunker 
from core.services.storage_manager import StorageManager
from core.services.tts.manager import TTSManager
from core.services.audio.merger import AudioMerger

from core.utils.constants import (EXTRACTED_TEXT,CLEAN_TEXT)

class NarrationPipeline:
    def __init__(self):
        self.extractor=PDFExtractor()
        self.cleaner=TextCleaner()
        self.preprocessor=TextPreprocessor()
        self.detector=ChapterDetector()
        self.chunker=TextChunker()
        self.storage=StorageManager()
        self.tts=TTSManager()
        self.merger=AudioMerger()

    def process(self,document:Document)->Document:
        self.storage.create(document)
        document=self.extractor.process(document)
        self.storage.save_text(document,EXTRACTED_TEXT,document.raw_text)
        document=self.cleaner.process(document)
        document=self.preprocessor.process(document)
        self.storage.save_text(document,CLEAN_TEXT,document.clean_text)
        document=self.detector.process(document)
        document=self.chunker.process(document)


        chunks_dir=(
            self.storage.root 
            / document.uuid 
            / "chunks"
        )

        audio_dir=self.storage.root / document.uuid / "audio"

        for chapter_index,chapter in enumerate(document.chapters,start=1):
            chapter_chunks_dir=(chunks_dir 
            / f"chapter_{chapter_index:02d}")

            chapter_audio_dir=(audio_dir 
            / f"chapter_{chapter_index:02d}")

            chapter_chunks_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            chapter_audio_dir.mkdir(
                parents=True,
                exist_ok=True
            )
            for chunk in chapter.chunks:
                
                chunk_text_path=(
                    chapter_chunks_dir
                    / f"chunk_{chunk.index:04d}.txt"
                )

                chunk_text_path.write_text(
                    chunk.text,
                    encoding="utf-8"
                )

                output_path=(
                    chapter_audio_dir 
                    / f"chunk_{chunk.index:04d}.wav")
                self.tts.generate(chunk,
                str(output_path)
                )

            chunk_audio_files=sorted(
                chapter_audio_dir.glob("chunk_*.wav")
            )
            chapter_audio_path=(
                audio_dir / f"chapter_{chapter_index:02d}.wav"
            )

            self.merger.merge(
                chunk_audio_files,
                chapter_audio_path
            )

        chapter_audio_files=sorted(
            audio_dir.glob("chapter_*.wav")
        ) 

        audiobook_path=(
            audio_dir / "audiobook.wav"
        )

        self.merger.merge(
            chapter_audio_files,
            audiobook_path
        )
        return document