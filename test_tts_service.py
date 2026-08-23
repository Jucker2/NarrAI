from core.domaine.chunk import Chunk
from core.services.tts.manager import TTSManager

chunk=Chunk(
    index=0,
    text="Bonjour, ceci est un test de NarrAI avec le moteur Kokoro."
)

manager=TTSManager()

print("Test: appel de manager.generate()")
output=manager.generate(
    chunk,
    "test_output/narration.wav"
)

print(f"Audio généré : {output}")