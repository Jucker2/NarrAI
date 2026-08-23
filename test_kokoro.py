from kokoro import KPipeline
import soundfile as sf

pipeline=KPipeline(lang_code="f")
text="""
Bonjour et bienvenue dans NarrAI.
Ceci est notre premier test de synthèse vocale.
Nous vérifions notamment la ponctuation,les pauses et le naturel de la voix.
"""
generator=pipeline(
    text,
    voice="ff_siwis",
    speed=1.0
)

for i ,(gs,ps,audio) in enumerate(generator):
    output=f"test_kokoro_{i}.wave"
    sf.write(output,audio,24000,format="WAV")
    print(f"Audio genere: {output}")