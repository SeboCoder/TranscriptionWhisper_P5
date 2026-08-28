# Automatische Videotranskription mit whisper.cpp

Das Python-Skript `transcribe_videos.py` verarbeitet alle unterstützten
Videodateien aus dem Ordner `inputVideo` alphabetisch. Für jedes Video wird
das Audio extrahiert, für Whisper konvertiert und anschließend mit dem
deutschen Modell `ggml-large-v3-turbo.bin` transkribiert.

## Voraussetzungen

Die benötigten Dateien müssen an diesen Stellen liegen:

```text
Prototyp5/
├── ffmpeg.exe
├── transcribe_videos.py
└── whisper/
	├── whisper-cli.exe
	└── models/
		└── ggml-large-v3-turbo.bin
```

FFmpeg wird direkt als `ffmpeg.exe` aus dem Projektordner verwendet. Eine
Installation oder ein Eintrag von FFmpeg im PATH ist daher nicht erforderlich.

## Verwendung

1. Videodateien in den Ordner `inputVideo` kopieren.
2. Das Skript aus dem Projektordner starten:

```powershell
python .\transcribe_videos.py
```

Das Skript kann auch gestartet werden, wenn das aktuelle Terminal in einem
anderen Ordner geöffnet ist, sofern der Pfad zum Skript angegeben wird.

## Verarbeitung

Für jedes Video führt das Skript diese Schritte aus:

1. Das Audio wird mit FFmpeg als Mono-WAV mit 16 kHz und 16-bit kodiert.
2. Whisper.cpp transkribiert die Audiodatei auf Deutsch.
3. Die JSON-Datei wird in den Ordner `result` verschoben.

Unterstützte Videoformate sind:
`.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.m4v`, `.mts` und `.m2ts`.

Beispiel:

```text
inputVideo\Unterricht.mp4
```

wird als folgende Datei gespeichert:

```text
result\Unterricht_transcription.json
```

## Temporäre Dateien

Während der Verarbeitung wird die Audiodatei
`whisper\input\Audio.wav` verwendet. Whisper erzeugt dort außerdem
`Audio.wav.json`. Beide Dateien werden vor dem nächsten Video gelöscht bzw.
überschrieben. Die fertigen Transkriptionen bleiben im Ordner `result` erhalten.

Existiert bereits eine Ergebnisdatei mit demselben Namen, wird sie durch die
neue Transkription ersetzt.