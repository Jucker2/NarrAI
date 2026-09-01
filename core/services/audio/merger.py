from pathlib import Path
import subprocess

from core.exceptions import AudioMergerError

class AudioMerger:
    def merge(self,input_files,output_path):
        """
        Assemble plusieur wav en un seul.
        input_files:liste de chemins vers les fichiers waves/
        output_path: chemindu wave du wave final
        """

        input_files=[
            Path(path)
            for path in input_files
        ]
        output_path=Path(output_path)
        if not input_files:
            raise ValueError(
                "Aucun fichier audio à assembler."
            )
        for path in input_files:
            if not path.exists():
                raise FileNotFoundError(
                    f"Fichier audio introuvable: {path}"
                )
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        concat_file=output_path.parent / "concat.txt"
        try:
            with concat_file.open("w",encoding="utf-8") as file:
                for path in input_files:
                    file.write(
                        f"file '{path.resolve().as_posix()}'\n"
                    )

            command=[
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",
                str(output_path)
            ]

            try:
                result= subprocess.run(
                    command,
                    capture_output=True,
                    text=True
                )
            except FileNotFoundError as exc:
                raise AudioMergerError(
                    "FFmpeg est introuvable. "
                    " vérifier que FFmeg est installé et accessible dans le PATH."
                ) from exc
            if result.returncode != 0:
                raise AudioMergerError(
                    f"echec de la fusion audio avec FFmeg:\n"
                    f"{result.stderr.strip()}"
                )
        finally:
            if concat_file.exists():
                concat_file.unlink()
        return output_path
            