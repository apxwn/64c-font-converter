# 64c font converter
Converts binary 64c font files to per-char PNG images with preview image. Generates image file for Pygame font engine by @DaFluffyPotato.

64c binary fonts can be found, for example, at http://home-2002.code-cop.org/c64/

---

Konvertiert c64-Zeichensätze (binäres *.64c-Format) pro Zeichen zu PNG und erstellt Preview. Erstellt Font-Image für Pygame font engine von @DaFluffyPotato.

**Aufruf:**
`biny.py 64c-Datei [Breite des Previewbilds in Zeichen] [Skalierungsfaktor des Previewbilds]`

Zum Beispiel:
`biny.py default.64c 32 2`

ergibt:

PNG-Dateien pro Zeichen aus default.64c, Previewbild mit einer Breite aus 32 Zeichen, 2-fach vergrößert, `fluffyfont.png` zur Verwendung mit Pygame font engine von DaFluffyPotato.

**Ausgabe:**

* result/{Dateiname des c64-Fonts}/'{index}. {hex.screencode}-{hex.petsciicode}.png'
* result/{Dateiname des c64-Fonts}/_preview.png
* result/{Dateiname des c64-Fonts}/fluffyfont.png

**Fluffyfont PNG image assumes:**

* monospaced font with height, width = 8 Pixels, as typical for c64 fonts,
* color=BLACK as transparent,
* split lines with color code (127, 127, 127).

If the original c64 font doesn't include more than one case, the one font case present will be doubled for both cases in `fluffyfont.png`.

If necessary, adjust `fluffy_character_order` according to your project.

Achtung! Skalierungsfaktor für das Preview geht nur als drittes Argument, also nicht ohne die Angabe der Breite des Previewbilds.

Die ersten beiden Byte von 64c-Dateien sind keine Inhalte. Falls dies im Einzelfall anders sein sollte, kann man den Offset (dz. 2) in Zeile 42 anpassen:

`recs = np.fromfile(f, dtype=rectype, offset=2)`

