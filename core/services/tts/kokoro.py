from pathlib import Path
import numpy as np
import soundfile as sf
from kokoro import KPipeline

from core.services.tts.base import BaseTTS
from core.domaine.chunk import Chunk


class KokoroTTS(BaseTTS):

    def __init__(self):
        self.pipeline=KPipeline(lang_code="f")

    def generate(self, chunk, output_path):
        print("test: entree dans kokoro")
        output_path=Path(output_path)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        generator=self.pipeline(
            chunk.text,
            voice="ff_siwis",
            speed=1.0
        )


        audio_parts=[]
        for _,_, audio in generator:
            audio_parts.append(audio)

        if not audio_parts:

            raise RuntimeError("kokoro n'a généré aucun audio."
            )

        audio=np.concatenate(audio_parts)
        sf.write(
            output_path,
            audio,
            24000,
        format="WAV"
        )

        return str(output_path)
