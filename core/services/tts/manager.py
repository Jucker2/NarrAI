from core.services.tts.kokoro import KokoroTTS

class TTSManager:
    def __init__(self):
        self.engine = KokoroTTS()

    def generate(self, chunk, output_path):
        return self.engine.generate(chunk, output_path)