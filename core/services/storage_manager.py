from pathlib import Path
import shutil
from core.domaine.document import Document


class StorageManager:
    def __init__(self,root="storage"):
        self.root=Path(root)

    def create(self,document:Document)->Path:
        book=self.root / document.uuid
        (book / "chunks").mkdir(parents=True,exist_ok=True)
        (book / "audio").mkdir(parents=True,exist_ok=True)

        return book

    def save_text(self,document:Document,filename:str,text:str):
        path=self.root / document.uuid / filename

        path.write_text(text,encoding="utf-8")

        return path

    def read_text(self,document:Document,filename:str):
        path=self.root / document.uuid / filename

        return path.read_text(encoding="utf-8")

    def delete(self,document:Document):
        path=self.root / document.uuid

        if path.exists():
            shutil.rmtree(path) 