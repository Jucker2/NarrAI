from abc import ABC, abstractmethod
from core.domaine.chunk import Chunk

class BaseTTS(ABC):
    @abstractmethod
    def generate(self, chunk: Chunk,output_path:str):
        pass