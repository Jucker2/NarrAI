from dataclasses import dataclass,field
from typing import List
from uuid import uuid4
from .chapter import Chapter

@dataclass
class Document:
    title:str
    pdf_path:str
    uuid:str=field(default_factory=lambda:str(uuid4()))

    author:str=""
    language:str=""
    raw_text:str=""
    clean_text:str=""

    chapters:List[Chapter]=field(default_factory=list)

    def to_dict(self):
        return{
            "uuid":self.uuid,
            "title":self.title,
            "author":self.author,
            "language":self.language,
            "raw_text":self.raw_text,
            "clean_text":self.clean_text,
            "chapters":[chapter.to_dict() for chapter in self.chapters]

        }