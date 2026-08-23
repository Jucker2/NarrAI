from dataclasses import dataclass

@dataclass
class Chunk:
    index:int
    text:str


    def to_dict(self):
        return{
            "index":self.index,
            "text":self.text,

        }