"""Extrahiert Audio aus Videos und transkribiert es mit whisper.cpp.

Alle unterstützten Videodateien im Ordner ``inputVideo`` werden alphabetisch
verarbeitet. Die fertigen Transkriptionen werden als JSON-Dateien im Ordner
``result`` abgelegt.
"""

from pathlib import Path
import subprocess


# Projektordner und Ein-/Ausgabeordner.
PROJECT_DIR = Path(__file__).resolve().parent
INPUT_VIDEO_DIR = PROJECT_DIR / "inputVideo"
WHISPER_DIR = PROJECT_DIR / "whisper"
WHISPER_INPUT_DIR = WHISPER_DIR / "input"
RESULT_DIR = PROJECT_DIR / "result"

# Externe Programme, Whisper-Modell und temporaere Dateien.
FFMPEG = PROJECT_DIR / "ffmpeg.exe"
WHISPER_CLI = WHISPER_DIR / "whisper-cli.exe"
MODEL = WHISPER_DIR / "models" / "ggml-large-v3-turbo.bin"
WHISPER_AUDIO = WHISPER_INPUT_DIR / "Audio.wav"
WHISPER_JSON = WHISPER_INPUT_DIR / "Audio.wav.json"

# Dateiendungen, die als Eingabevideos verarbeitet werden.
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".mts", ".m2ts"}


def run_command(command: list[str], working_directory: Path) -> None:
    """Fuehrt einen externen Prozess im angegebenen Arbeitsordner aus.

    Args:
        command: Programm und Argumente als Liste.
        working_directory: Ordner, in dem der Prozess gestartet wird.

    Raises:
        subprocess.CalledProcessError: Wenn der Prozess mit einem Fehler endet.
    """
    subprocess.run(command, cwd=working_directory, check=True)


def extract_audio(video_path: Path) -> None:
    """Extrahiert das Audiosignal eines Videos als Whisper-kompatible WAV-Datei.

    Das Audio wird auf einen Kanal und eine Abtastrate von 16 kHz konvertiert.

    Args:
        video_path: Pfad zum Eingabevideo.
    """
    run_command(
        [
            FFMPEG,
            "-y",
            "-i",
            str(video_path),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "pcm_s16le",
            str(WHISPER_AUDIO),
        ],
        PROJECT_DIR,
    )


def transcribe_audio() -> None:
    """Transkribiert die temporaere WAV-Datei mit dem deutschen Whisper-Modell."""
    run_command(
        [
            str(WHISPER_CLI),
            "-m",
            str(MODEL),
            "-l",
            "de",
            "-f",
            "input\\Audio.wav",
            "-oj",
        ],
        WHISPER_DIR,
    )


def main() -> None:
    """Prueft die Voraussetzungen und verarbeitet alle Eingabevideos."""
    # Ohne diese Dateien koennen die beiden Verarbeitungsschritte nicht starten.
    if not INPUT_VIDEO_DIR.exists():
        raise FileNotFoundError(f"Input-Ordner nicht gefunden: {INPUT_VIDEO_DIR}")
    if not WHISPER_CLI.exists():
        raise FileNotFoundError(f"Whisper-CLI nicht gefunden: {WHISPER_CLI}")
    if not MODEL.exists():
        raise FileNotFoundError(f"Whisper-Modell nicht gefunden: {MODEL}")
    if not FFMPEG.exists():
        raise FileNotFoundError(
            f"FFmpeg wurde nicht gefunden: {FFMPEG}"
        )

    # Ausgabe- und Whisper-Eingabeordner bei Bedarf automatisch anlegen.
    RESULT_DIR.mkdir(exist_ok=True)
    WHISPER_INPUT_DIR.mkdir(exist_ok=True)

    # Die alphabetische Reihenfolge sorgt fuer einen reproduzierbaren Ablauf.
    videos = sorted(
        (
            path
            for path in INPUT_VIDEO_DIR.iterdir()
            if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS
        ),
        key=lambda path: path.name.lower(),
    )

    if not videos:
        print(f"Keine Videodateien in {INPUT_VIDEO_DIR} gefunden.")
        return

    for video_path in videos:
        print(f"\nVerarbeite: {video_path.name}")

        # Whisper verwendet immer dieselben temporaeren Dateinamen.
        WHISPER_AUDIO.unlink(missing_ok=True)
        WHISPER_JSON.unlink(missing_ok=True)

        extract_audio(video_path)
        transcribe_audio()

        # Das Ergebnis bekommt den Namen des Videos ohne Dateiendung.
        output_path = RESULT_DIR / f"{video_path.stem}_transcription.json"
        WHISPER_JSON.replace(output_path)
        print(f"Gespeichert: {output_path}")


if __name__ == "__main__":
    main()