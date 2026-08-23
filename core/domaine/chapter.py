from dataclasses import dataclass,field
from typing import List
from .chunk import Chunk

@dataclass
class Chapter:
    title:str
    content:str
    chunks:List[Chunk]=field(default_factory=list)

    def to_dict(self):
        return{
            "title":self.title,
            "content":self.content,
            "chunks":[chunk.to_dict() for chunk in self.chunks]

        }