# 64c font converter
Converts binary 64c font files to per-char PNG images with preview image.

64c fonts can be found, for example, at http://home-2002.code-cop.org/c64/

---

Konvertiert c64-Zeichensätze (*.64c-Format) pro Zeichen zu PNG und erstellt Preview.

Aufruf:
`biny.py 64c-Datei [Breite des Previewbilds in Zeichen] [Skalierungsfaktor des Previewbilds]`

Zum Beispiel:
`biny.py default.64c 32 2`

ergibt:

PNG-Dateien pro Zeichen aus default.64c, Previewbild mit einer Breite aus 32 Zeichen, 2-fach vergrößert.

Achtung! Skalierungsfaktor geht nur als drittes Argument, also nicht ohne die Angabe der Breite des Previewbilds.

Die ersten beiden Byte von 64c-Dateien sind keine Inhalte. Falls dies anders sein sollte, kann man den Offset (dz. 2) in Zeile 25 anpassen.
