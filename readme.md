# Automatische Videotranskription mit Whisper

## Überblick

Dieser Prototyp untersucht, wie sich Videodateien lokal und automatisiert in
Text umwandeln lassen. Das Python-Skript `transcribe_videos.py` durchsucht den
Eingabeordner `inputVideo`, extrahiert aus jedem unterstützten Video die
Audiospur und erzeugt im Ordner `result` eine JSON-Transkription.

Die Verarbeitung läuft lokal auf dem eigenen Rechner. Die Video- und
Audiodateien müssen daher nicht an einen externen Transkriptionsdienst
übertragen werden. Der Prototyp konzentriert sich zunächst auf die Usability:
Videos ablegen, Skript starten und Ergebnisse erhalten.

## Entstehung und Wahl der Technologie

### Erster Ansatz: Whisper mit Transformers

Bei der Recherche auf [Hugging Face](https://huggingface.co/) wurden Modelle
für Speech-to-Text (STT), also automatische Spracherkennung (ASR), untersucht.
Whisper ist in diesem Bereich ein besonders verbreitetes Modell. Deshalb wurde
zunächst versucht, Whisper über die Python-Bibliothek
[Transformers](https://huggingface.co/docs/transformers/en/model_doc/whisper)
lokal auszuführen.

Eine Ausführung auf der CPU war einmal erfolgreich. Die Nutzung der GPU ließ
sich jedoch nicht stabil einrichten. Dabei traten wiederholt
Abhängigkeitsprobleme zwischen Python, PyTorch, CUDA und dem CUDA Toolkit auf.
Mehrere virtuelle Umgebungen (`venv`) mit unterschiedlichen
Abhängigkeitskombinationen führten ebenso wenig zu einer zuverlässigen Lösung
wie ein Versuch auf einem frisch eingerichteten Leih-Laptop.

Diese Erfahrung zeigt eine praktische Hürde des Transformers-Ansatzes: Neben
dem Modell selbst müssen die passende Python-, PyTorch-, CUDA- und
Treiberkonfiguration zusammenpassen. Für einen ersten Usability-Prototypen war
dieser Installations- und Wartungsaufwand zu hoch.

### Zweiter Ansatz: whisper.cpp

Um den eigentlichen Transkriptionsablauf trotzdem testen zu können, fiel die
Wahl auf [whisper.cpp](https://github.com/ggml-org/whisper.cpp). Dabei handelt
es sich um eine schlanke C/C++-Implementierung von OpenAIs Whisper-Modell, die
unter anderem ein fertiges Kommandozeilenprogramm (`whisper-cli`) bereitstellt.
Whisper.cpp unterstützt sowohl CPU-only-Inferenz als auch verschiedene
Möglichkeiten zur GPU-Beschleunigung. Für diesen Prototyp wird das vorhandene
CLI-Programm lokal verwendet; eine funktionierende GPU-Konfiguration ist für
den beschriebenen Ablauf nicht erforderlich.

Ein weiterer Vorteil ist die einfache Dateiverarbeitung: `whisper-cli` kann
das Ergebnis direkt als JSON-Datei ausgeben. Dadurch kann das Python-Skript den
Transkriptionsprozess automatisieren, ohne die Ausgabe erst aus einer
Konsolenansicht herausparsen zu müssen.

## Modell

Verwendet wird das mehrsprachige Modell `ggml-large-v3-turbo.bin`. Die Wahl
fiel auf dieses Modell, weil es neben Deutsch auch viele weitere europäische
Sprachen unterstützt und als Large-v3-Turbo-Variante ein gutes Verhältnis
zwischen Modellgröße, Geschwindigkeit und erwarteter Erkennungsqualität
bietet.

Whisper.cpp verwendet ein eigenes, GGML-basiertes binäres Modellformat. Die
ursprünglichen Whisper-Modelle können daher nicht einfach unverändert mit
whisper.cpp verwendet werden, sondern müssen konvertiert werden. Für das hier
verwendete Modell ist dieser Schritt bereits erledigt: Auf der
[Hugging-Face-Modellseite von whisper.cpp](https://huggingface.co/ggerganov/whisper.cpp/tree/main)
steht `ggml-large-v3-turbo.bin` als fertig konvertiertes Modell zum Download
bereit.

Das Modell ist mit ungefähr 1,62 GB relativ groß. Es muss nur einmal in den
Ordner `whisper\models` heruntergeladen werden und bleibt anschließend lokal
verfügbar.


## Projektstruktur und Voraussetzungen

Die benötigten Dateien müssen an diesen Stellen liegen:

```text
TranscriptionWhisper_P5/
├── ffmpeg.exe
├── transcribe_videos.py
├── inputVideo/
├── result/
└── whisper/
	 ├── whisper-cli.exe
	 ├── input/
	 └── models/
		  └── ggml-large-v3-turbo.bin
```

## Große Dateien und Release-Version

Die größeren Dateien, insbesondere die KI-Modelle und `ffmpeg.exe`, sind aus
Gründen der Dateigröße nicht Bestandteil des GitHub-Repositories.

Unter [Releases](../../releases) steht eine installierbare Version des
Prototyps bereit. In dieser Version ist FFmpeg bereits enthalten. Für die
vollständige Einrichtung muss lediglich das Modell
`ggml-large-v3-turbo.bin` heruntergeladen und in den Ordner
`whisper\models` kopiert werden. Danach kann das Skript entsprechend der
Anleitung gestartet werden.

Benötigt werden:

- Python 3 für das Skript
- `ffmpeg.exe` im Projektordner
- `whisper-cli.exe` im Ordner `whisper`
- das Modell `ggml-large-v3-turbo.bin` im Ordner `whisper\models`

FFmpeg wird direkt aus dem Projektordner verwendet. Eine separate Installation
oder ein Eintrag von FFmpeg im `PATH` ist daher nicht erforderlich.

## Verwendung

1. Videodateien in den Ordner `inputVideo` kopieren.
2. Ein PowerShell-Terminal im Projektordner öffnen.
3. Das Skript starten:

```powershell
python .\transcribe_videos.py
```

Das Skript kann auch aus einem anderen aktuellen Verzeichnis gestartet werden,
wenn der Pfad zum Skript angegeben wird.

## Verarbeitung

Für jedes Video führt das Skript diese Schritte aus:

1. Die Videos im Ordner `inputVideo` werden alphabetisch sortiert.
2. FFmpeg extrahiert die Audiospur und konvertiert sie in eine einkanalige
	WAV-Datei mit 16 kHz und 16 Bit (`pcm_s16le`). Dieses Format entspricht den
	Anforderungen von `whisper-cli`.
3. Whisper.cpp transkribiert die WAV-Datei mit der Spracheinstellung Deutsch.
4. Whisper.cpp erzeugt mit der Option `-oj` eine JSON-Datei.
5. Das Python-Skript verschiebt die JSON-Datei nach `result` und benennt sie
	nach dem ursprünglichen Videonamen.

Unterstützte Videoformate sind `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.m4v`,
`.mts` und `.m2ts`.

Beispiel:

```text
inputVideo\Unterricht.mp4
```

wird als folgende Datei gespeichert:

```text
result\Unterricht_transcription.json
```

## Temporäre Dateien und Überschreiben

Während der Verarbeitung verwendet das Skript die temporären Dateien
`whisper\input\Audio.wav` und `whisper\input\Audio.wav.json`. Diese Dateien
werden vor dem nächsten Video gelöscht beziehungsweise überschrieben. Die
fertigen Transkriptionen bleiben im Ordner `result` erhalten.

Existiert bereits eine Ergebnisdatei mit demselben Namen, wird sie durch die
neue Transkription ersetzt.

## Einordnung des Prototyps

Der aktuelle Stand ist ein funktionaler Prototyp und noch keine vollständige
Produktionslösung. Im Mittelpunkt stehen die lokale Ausführung, die
automatische Stapelverarbeitung mehrerer Videos und die strukturierte
JSON-Ausgabe. Themen wie eine Benutzeroberfläche, Fortschrittsanzeige,
Fehlerprotokollierung, Sprechererkennung und ein systematischer Vergleich von
Modellvarianten können darauf aufbauend ergänzt werden.

## Hinweis zu den Testdateien

Das Repository enthält Testdateien, die während der Entwicklung zum Prüfen des
Transkriptionsablaufs verwendet wurden. Diese Dateien dienen ausschließlich
dem Testen des Prototyps und sollen nicht außerhalb des vorgesehenen
Projektkontexts weitergegeben oder veröffentlicht werden.


## Hinweis zur Erstellung

Bei der Recherche, beim Verfassen dieser Dokumentation und bei der Erstellung
des Codes wurden Large Language Models (LLMs) unterstützend eingesetzt. Die
Vorschläge wurden anschließend geprüft, an die Anforderungen des Projekts
angepasst und praktisch getestet. Die fachliche Einordnung sowie die
Verantwortung für den finalen Text und den veröffentlichten Code liegen beim
Verfasser.


## Weiterführende Quellen

- [Whisper-Dokumentation in Transformers](https://huggingface.co/docs/transformers/en/model_doc/whisper)
- [whisper.cpp auf GitHub](https://github.com/ggml-org/whisper.cpp)
- [Konvertierte whisper.cpp-Modelle auf Hugging Face](https://huggingface.co/ggerganov/whisper.cpp/tree/main)

## Urhebernachweis

Sebastian Heiden, Masterstudent an der USTP – University of Applied Sciences St. Pölten
August 2026