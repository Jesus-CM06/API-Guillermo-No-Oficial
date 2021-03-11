def cleanup_Capitals(text): # 65 al 90 + 209 de "Ñ" + 32 de " "
	return "".join([c if ord(c) == 32 or ord(c) >= 65 and ord(c)<= 90 or ord(c) == 209  else "" for c in text]).strip()

def cleanup_Numbers(text): # 48 al 57 + 32 de " "
	return "".join([c if ord(c) == 32 or ord(c) >=48 and ord(c)<= 57 else "" for c in text]).strip()

def cleanup_CapitalsAndNumbers(text): # 48 al 57 + 65 al 90 + 209 de "Ñ"
	return "".join([c if ord(c) >=48 and ord(c)<= 57 or ord(c) >= 65 and ord(c)<= 90 or ord(c) == 209 else "" for c in text]).strip()

def cleanup_AddressValues(text): # 48 al 57 + 65 al 90 + 209 de "Ñ" + 44 "," + 46 "." + 32 de " "
	return "".join([c if ord(c) == 32 or ord(c) == 44 or ord(c) >=46 and ord(c)<= 57 or ord(c) >= 65 and ord(c) <= 90 or ord(c) == 209 else "" for c in text]).strip()

def cleanup_DateValues(text): # 47 al 57 (47 "/")
	return "".join([c if ord(c) >=47 and ord(c)<= 57 else "" for c in text]).strip()

def cleanup_BackID(text): # 48 al 57 + 65 al 90 + 209 de "Ñ" + 60 "<" + 10 de "enter"
	return "".join([c if ord(c) == 10 or ord(c) >=48 and ord(c)<= 57 or ord(c) == 60 or ord(c) >= 65 and ord(c)<= 90 or ord(c) == 209 else "" for c in text]).strip()

def cleanup_CURP(text):
	clean = ''
	for i in range(len(text)):
		if i >= 0 and i <= 3 or i >= 10 and i <= 15:
			cleanChar = intToChar(text[i])
		if i >= 4 and i <= 9 or i >= 16 and i <= 17:
			if i == 16 and text[i] == 'A':
				cleanChar = text[i]
			else:
				cleanChar = charToInt(text[i])
		clean = clean + str(cleanChar)
	return clean

def cleanup_Key(text):
	clean = ''
	for i in range(len(text)):
		if i >= 0 and i <= 5 or i == 14:
			cleanChar = intToChar(text[i])
		if i >= 6 and i <= 13 or i >= 15 and i <= 17:
			cleanChar = charToInt(text[i])
		clean = clean + str(cleanChar)
	return clean

def cleanup_stringBackID(text):
	clean = ''
	for i in range(len(text)):
		if i >= 0 and i <= 4:
			cleanChar = intToChar(text[i])
		if i >= 5 and i <= 14 or i >= 17 and i <= 29:
			cleanChar = charToInt(text[i])
		if i >= 15 and i <= 16:
			cleanChar = "<"
		clean = clean + str(cleanChar)
	return clean

def intToChar(element):
	cleanChar = element
	if element == '0':
		cleanChar = 'O'
	elif element == '1':
		cleanChar = 'I'
	elif element == '3':
		cleanChar = 'E'
	elif element == '4':
		cleanChar = 'A'
	elif element == '5':
		cleanChar = 'S'
	elif element == '6':
		cleanChar = 'G'
	elif element == '8':
		cleanChar = 'B'

	return cleanChar

def charToInt(element):
	cleanChar = element
	if element == 'A':
		cleanChar = '4'
	elif element == 'B':
		cleanChar = '8'
	elif element == 'D':
		cleanChar = '0'
	elif element == 'E':
		cleanChar = '3'
	elif element == 'G':
		cleanChar = '6'
	elif element == 'I':
		cleanChar = '1'
	elif element == 'O':
		cleanChar = '0'
	elif element == 'Q':
		cleanChar = '0'
	elif element == 'S':
		cleanChar = '5'
	elif element == 'T':
		cleanChar = '1'

	return cleanChar
