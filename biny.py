import numpy as np
import pygame, sys, os
import json, logging
from pygame.locals import *
from PIL import Image, ImageOps

# Logging
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename='biny.log', encoding='utf-8', level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger('biny')

json_file = open("charmap.json")
charmap = json.load(json_file)
json_file.close()

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
# output file name format: '{index}. {hex.screencode}-{hex.petsciicode}.png'

def char_to_img(filename, invert=False):
	f = open(filename)
	logger.info("--- Versuche, Zeichensatz aus Datei " + filename + " zu generieren.")
	filesize = os.stat(filename).st_size
	logger.info(filename + " ist " + str(filesize) + " Byte groß.")
	auffuellen = filesize - 729
	if auffuellen < 0:
		logger.info("Daher wird der Zeichensatz für Fluffyfont auf die Kleinbuchstaben verdoppelt.")
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

	return zeichensatz, auffuellen

def make_preview(zeichensatz, breite=16, scale=1):
	# breite: Breite in Zeichen, nicht in Pixeln
	# scale: Skalierung des Previewbilds
	hoehe = int(len(zeichensatz) / breite) + 1
	preview = Image.new('1', (breite * 8, hoehe * 8))
	fluffy_character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
	fluffy_font = Image.new('RGB', (len(fluffy_character_order)*9, 8))

	fluffy_screencode = 0
	xoffset = 0
	yoffset = 0
	for char in zeichensatz:
		preview.paste(char, (xoffset, yoffset))
		xoffset += char.width
		if xoffset >= breite * 8:
			xoffset = 0
			yoffset += char.height

		petsciicode, asciicode = get_petscii(fluffy_screencode)
		if chr(asciicode) not in fluffy_character_order:
			# skippe dieses Zeichen bei fluffy_font
			logger.debug("Fluffy hat kein " + chr(asciicode) + "!")
			fluffy_screencode += 1
			continue
		fluffy_position = fluffy_character_order.index(chr(asciicode))
		fluffy_xoffset = fluffy_position * 9 # ein Zeichen ist 8 Pixel breit plus ein Pixel Trennlinie
		fluffy_char = char.convert('L')
		fluffy_char = ImageOps.invert(fluffy_char)
		fluffy_font.paste(fluffy_char, (fluffy_xoffset, 0))

		fluffy_screencode += 1
	if auffuellen <= 0:
		fluffy_screencode = 0
		for char in zeichensatz:
			if fluffy_screencode < 1 or fluffy_screencode > 26 or chr(asciicode).swapcase() not in fluffy_character_order:
				fluffy_screencode += 1
				continue
			petsciicode, asciicode = get_petscii(fluffy_screencode)

			fluffy_position = fluffy_character_order.index(chr(asciicode).swapcase())
			fluffy_xoffset = fluffy_position * 9
			fluffy_char = char.convert('L')
			fluffy_char = ImageOps.invert(fluffy_char)
			fluffy_font.paste(fluffy_char, (fluffy_xoffset, 0))
			fluffy_screencode += 1

	# 127er-Linien malen
	fluffy_xoffset = 8 # erste Linie bei X = 8
	while fluffy_xoffset < fluffy_font.width:
		fluffy_yoffset = 0
		while fluffy_yoffset < 8:
			fluffy_font.putpixel((fluffy_xoffset, fluffy_yoffset), (127,127,127))
			fluffy_yoffset += 1
		fluffy_xoffset += 9 # ein Zeichen ist 8 Pixel breit plus ein Pixel Trennlinie

	preview = preview.resize((scale * preview.width, scale * preview.height))
	return preview, fluffy_font

def get_petscii(screencode): # konvertiert c64-Screencode zu Petscii und Ascii aus charmap.json
	petsciicode = charmap[str(screencode)][0]
	asciicode = charmap[str(screencode)][1]
	return petsciicode, asciicode

args = sys.argv
if len(args) == 1:
	print ("Du hast mir nicht den Namen der Zeichensatzdatei gegeben.\n\n")
	logger.info("Aufruf ohne Kommandozeilenparameter. Beende.")
	print (hilfetext)
	exit()
inputdatei = args[1]
try:
	preview_breite = int(args[2])
except:
	preview_breite = 16
try:
	preview_skalierung = int(args[3])
except:
	preview_skalierung = 1

if not os.path.exists('result'):
	os.mkdir('result')
ausgabepfad = 'result/' + inputdatei
if not os.path.exists(ausgabepfad):
	os.mkdir(ausgabepfad)

zeichensatz, auffuellen = char_to_img(inputdatei, True)
preview, fluffyfont = make_preview(zeichensatz, preview_breite, preview_skalierung)
preview.save(ausgabepfad + '/_preview.png')
fluffyfont.save(ausgabepfad + '/fluffyfont.png')

i = 0
screencode = 0
for char in zeichensatz:
	petsciicode, asciicode = get_petscii(screencode)
	fname = ausgabepfad + '/' + str(i).zfill(3) + ". " + str(hex(screencode)[2:]).zfill(2) + "-" + str(hex(petsciicode)[2:]).zfill(2) + ".png"
	char.save(fname)
	screencode += 1
	i += 1
