from pathlib import Path
import wave
from django.test import TestCase

from core.services.audio.merger import AudioMerger

class AudioMergerTests(TestCase):

    def test_merge_audio_files(self):

        audio_dir = Path("storage/test_audio")
        audio_dir.mkdir(parents=True,exist_ok=True)

        input_files =[]

        for i in range(2):
            path=audio_dir / f"test_{i}.wav"
            with wave.open(str(path),"w") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(22050)
                wav.writeframes(b"\x00\x00" * 22050)

            input_files.append(path)
        

        self.assertGreaterEqual(
            len(input_files),
            2,
            "Il faut au moins deux fichiers WAV dans storage/test_audio/"
        )

        output_path = audio_dir / "merged.wav"

        merger = AudioMerger()

        result = merger.merge(
            input_files,
            output_path
        )

        self.assertTrue(
            result.exists(),
            "Le fichier merged.wav n'a pas été créé."
        )

        self.assertGreater(
            result.stat().st_size,
            0,
            "Le fichier merged.wav est vide."
        )

        print(
            f"\nAudio assemblé : {result}"
        )