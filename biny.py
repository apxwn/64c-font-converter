import numpy as np
import sys
from PIL import Image

hilfetext = """Konvertiert c64-Zeichensätze (*.64c-Format) pro Zeichen zu PNG und erstellt Preview.

Aufruf:
biny.py 64c-Datei [Breite des Previewbilds in Zeichen] [Skalierungsfaktor des Previewbilds]

Zum Beispiel:
biny.py default.64c 32 2
ergibt:

PNG-Dateien pro Zeichen aus default.64c, Previewbild mit einer Breite aus 32 Zeichen, 2-fach vergrößert.

Achtung! Skalierungsfaktor geht nur als drittes Argument, also nicht ohne die Angabe der Breite des Previewbilds.
"""

# input file: binary, *.64c format (c64 font)
# output file name format: '{index}. {hex.screencode}-{hex.asciicode}.png'

def char_to_img(filename, invert=False):
	f = open(filename)
	rectype = np.dtype({'names': ['0','1','2','3','4','5','6','7'], 'formats': [np.uint8, np.uint8, np.uint8, np.uint8, np.uint8, np.uint8, np.uint8, np.uint8]})
	recs = np.fromfile(f, dtype=rectype, offset=2)

	zeichensatz = []

	for char in recs:
		current_char = []
		if invert:
			for byte in char:
				current_char.append(np.invert(np.array(byte, dtype=np.uint8)))
		else:
			current_char = char
		zeichensatz.append(Image.frombytes('1', (8, 8), bytes(current_char)))

	return zeichensatz

def make_preview(zeichensatz, breite=16, scale=1):
	# breite: Breite in Zeichen, nicht in Pixeln
	# scale: Skalierung des Previewbilds
	hoehe = int(len(zeichensatz) / breite) + 1
	preview = Image.new('1', (breite * 8, hoehe * 8))
	xoffset = 0
	yoffset = 0
	for char in zeichensatz:
		preview.paste(char, (xoffset, yoffset))
		xoffset += char.width
		if xoffset >= breite * 8:
			xoffset = 0
			yoffset += char.height
	preview = preview.resize((scale * preview.width, scale * preview.height))
	return preview

args = sys.argv
if len(args) == 1:
	print ("Du hast mir nicht den Namen der Zeichensatzdatei gegeben.")
	print (hilfetext)
	exit()
inputdatei = args[1]
preview_breite = 16
preview_skalierung = 1
if args[2]:
	preview_breite = int(args[2])
if args[3]:
	preview_skalierung = int(args[3])

zeichensatz = char_to_img(inputdatei, True)
preview = make_preview(zeichensatz, preview_breite, preview_skalierung)
preview.save('preview.png')

i = 0
screencode = 0
for char in zeichensatz:
	if screencode < 32:
		asciicode = screencode + 64
	elif screencode < 64:
		asciicode = screencode
	elif screencode < 96:
		asciicode = screencode + 128
	elif screencode < 128:
		asciicode = screencode + 64
	elif screencode < 160:
		asciicode = screencode - 128
	elif screencode < 224:
		asciicode = screencode - 64
	elif screencode < 255:
		asciicode = screencode

	fname = str(i).zfill(3) + ". " + str(hex(screencode)[2:]).zfill(2) + "-" + str(hex(asciicode)[2:]).zfill(2) + ".png"
	char.save(fname)
	screencode += 1
	i += 1
