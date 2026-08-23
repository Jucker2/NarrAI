import re

from core.domaine.document import Document
from core.domaine.chunk import Chunk

class TextChunker:

    def __init__(self, max_chars=1000):
        self.max_chars = max_chars

    def process(self, document: Document) -> Document:

        for chapter in document.chapters:

            chapter.chunks = []

            chunk_index = 1

            paragraphs = [
                p.strip()
                for p in chapter.content.split("\n\n")
                if p.strip()
            ]

            current_chunk = ""

            for paragraph in paragraphs:

                # Cas normal : le paragraphe tient dans un chunk
                if len(paragraph) <= self.max_chars:

                    if len(current_chunk) + len(paragraph) + 2 <= self.max_chars:
                        current_chunk += paragraph + "\n\n"
                    else:
                        if current_chunk:
                            chapter.chunks.append(
                                Chunk(
                                    index=chunk_index,
                                    text=current_chunk.strip()
                                )
                            )
                            chunk_index += 1

                        current_chunk = paragraph + "\n\n"

                else:
                    # On vide le chunk courant
                    if current_chunk:
                        chapter.chunks.append(
                            Chunk(
                                index=chunk_index,
                                text=current_chunk.strip()
                            )
                        )
                        chunk_index += 1
                        current_chunk = ""

                    # Découpage par phrases
                    sentences = re.split(r'(?<=[.!?])\s+', paragraph)

                    temp = ""

                    for sentence in sentences:

                        # Phrase trop longue
                        if len(sentence) > self.max_chars:

                            if temp:
                                chapter.chunks.append(
                                    Chunk(
                                        index=chunk_index,
                                        text=temp.strip()
                                    )
                                )
                                chunk_index += 1
                                temp = ""

                            # Découpage forcé
                            for i in range(0, len(sentence), self.max_chars):
                                chapter.chunks.append(
                                    Chunk(
                                        index=chunk_index,
                                        text=sentence[i:i+self.max_chars]
                                    )
                                )
                                chunk_index += 1

                        else:

                            if len(temp) + len(sentence) + 1 <= self.max_chars:
                                temp += sentence + " "
                            else:
                                chapter.chunks.append(
                                    Chunk(
                                        index=chunk_index,
                                        text=temp.strip()
                                    )
                                )
                                chunk_index += 1
                                temp = sentence + " "

                    if temp:
                        chapter.chunks.append(
                            Chunk(
                                index=chunk_index,
                                text=temp.strip()
                            )
                        )

            if current_chunk:
                chapter.chunks.append(
                    Chunk(
                        index=chunk_index,
                        text=current_chunk.strip()
                    )
                )

        return document