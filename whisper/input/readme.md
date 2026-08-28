Versuch Whisper zu verwenden über whisper.cpp  https://github.com/ggml-org/whisper.cpp

# Installation:

release herunterladen: https://github.com/ggml-org/whisper.cpp/tree/master
modell im richtigen format herunterladen: https://huggingface.co/ggerganov/whisper.cpp/tree/main
modell im modelsordner ablegen

# Test1:

 .\whisper-cli.exe -m models\ggml-medium.bin -l de -f input\Audio1.wav -otxt

 Ausgabe:

[00:00:00.000 --> 00:00:05.000]   Da haben wir die Texas-Copmentarschkarte, oder?
[00:00:05.000 --> 00:00:09.000]   Das war die 2, die haben gefährlich verheiratet.
[00:00:09.000 --> 00:00:12.000]   Wo ist die Stängelin von?
[00:00:12.000 --> 00:00:14.000]   Da ist sie, ja sie ist, man sieht sie.
[00:00:14.000 --> 00:00:16.000]   Da wendest du sie natürlich.
[00:00:16.000 --> 00:00:21.000]   Und da war von Haus aus nichts abgedeckt.
[00:00:23.000 --> 00:00:28.000]   Und bei Harnitz haben wir sowieso, das heißt wir kennen uns auch nicht mit lange Haare.
[00:00:28.000 --> 00:00:38.000]   Aber das war natürlich blöd, wenn man sich da mit den Haaren ausgedeckt hat.
[00:00:38.000 --> 00:00:41.000]   Ja, ja, deswegen ja.

Fazit: Ganz gut hat aber nur CPU verwendet


# Test2:

 .\whisper-cli.exe -m models\ggml-large-v3-turbo.bin -l de -f input\Audio1.wav -otxt

 Ausgabe:

[00:00:00.000 --> 00:00:04.900]   "Da haben wir die Tessis-Kochmetallstuhl aus."
[00:00:04.900 --> 00:00:09.020]   "Die zwei werden sicherlich in der Höhe, ob ich nicht."
[00:00:09.020 --> 00:00:11.600]   "Da ist es egal, wie vor mir."
[00:00:11.600 --> 00:00:15.600]   "Da ist es, ja, die Tessis-Kochmetallstuhl, da geht es natürlich."
[00:00:15.600 --> 00:00:21.100]   "Ist aber von Haus aus nicht nachgedeckt."
[00:00:21.100 --> 00:00:29.400]   "Und bei Hanitz haben wir sowieso, das heißt, wir können uns auch nicht mit Lange-Halter im Poker hin und einzuspielen."
[00:00:29.400 --> 00:00:38.400]   "Aber die sind natürlich blöd, wenn sie da mit den Huren abzübt."
[00:00:38.400 --> 00:00:41.400]   "Ja, ja, ja, deswegen reicht."
[00:00:41.400 --> 00:00:47.500]   "Aber die sind natürlich blöd, wenn sie da mit den Huren abzübt."

Fazit: Nur Cpu aber lustigerweise schlechteres ergebnis als das medium modell

# Test3:

Test mit Audio2 (ist ein leichteres file)

Hier erscheint large eine bessere transkribtion zu generieren vorallem erkennt large den hauptsprecher und blendet die hintergrundstimme aus

medium:

[00:00:00.000 --> 00:00:06.980]   Wenn man den Vorhang beziehungsweise wenn man die Arbeitsplätze absaugen will?
[00:00:06.980 --> 00:00:11.800]   Ja, wir haben nur für zwei Arbeitsplätze eine Absaugung.
[00:00:11.800 --> 00:00:14.800]   Da kann man nur an zwei Arbeitsplätzen abschweißen.
[00:00:14.800 --> 00:00:19.240]   Also der Dritte muss eigentlich immer frei bleiben, dieser Platz.
[00:00:19.240 --> 00:00:26.220]   Weil du kannst ja nicht, du darfst auch nicht den Schweißvorhang wegnehmen,
[00:00:26.220 --> 00:00:35.560]   weil dann werden ja die Teilnehmer gegenseitig geblitzt und vom Lichtbogen belastet.
[00:00:35.560 --> 00:00:40.480]   Also an dieser Stelle kann man nur mit zwei Schweißplätzen arbeiten.

large:

[00:00:00.000 --> 00:00:11.600]   Wir haben nur für zwei Schweißarbeitsplätze eine Absaugung,
[00:00:11.600 --> 00:00:14.360]   können wir nur an zwei Arbeitsplätzen noch schweißen.
[00:00:14.980 --> 00:00:19.140]   Also der Dritte muss eigentlich immer frei bleiben, dieser Platz.
[00:00:19.580 --> 00:00:25.900]   Du darfst doch nicht den Schweißvorhang wegnehmen,
[00:00:25.900 --> 00:00:29.720]   weil dann werden ja die Teilnehmer gegenseitig geblitzt.
[00:00:30.000 --> 00:00:33.140]   Und vom Lichtbogen belastet.
[00:00:35.000 --> 00:00:38.840]   Also an dieser Stelle können wir nur mit zwei Schweißplätzen arbeiten.

# Automatische Videotranskription:

Das Skript `transcribe_videos.py` verarbeitet alle Videodateien aus dem Ordner `inputVideo` alphabetisch.
Für jedes Video wird das Audio mit FFmpeg als Mono-WAV mit 16 kHz exportiert und anschliessend mit
`ggml-large-v3-turbo.bin` transkribiert. Die fertigen JSON-Dateien werden im Ordner `result` gespeichert.

Voraussetzungen:

- FFmpeg muss installiert und im PATH enthalten sein.
- `whisper\models\ggml-large-v3-turbo.bin` muss vorhanden sein.

Start:

```powershell
python .\transcribe_videos.py
```

Beispiel: `inputVideo\Unterricht.mp4` wird als `result\Unterricht_transcription.json` gespeichert.

