import Functions.align_images as align_images
import numpy as np
import argparse
import imutils
import pytesseract
import cv2
import datetime
from collections import namedtuple
from PIL import Image as im
import tempfile
import Functions.delimitadores as dl
import Functions.gammaFunction as gf
import Functions.orientationFunctions as of
from Functions.OCRLocations import *

def alignDocFunction(image, template,typeID):

    initialTime = datetime.datetime.now()

    # Define a tuple to save OCR Locations
    OCRLocation = namedtuple("OCRLocation", ["id", "bbox", "filter_keywords"])
    OCR_LOCATIONS = []

    # Align new image to template
    aligned = align_images.align_images(image, template, debug=True)

    # Adjust images
    aligned = imutils.resize(aligned, width=700)
    alignedHeight, alignedWidth, c = aligned.shape
    image = imutils.resize(image, height = alignedHeight)
    template = imutils.resize(template, width=700)

    # Update OCR Locations according the type of document
    if typeID == 0:
        OCR_LOCATIONS = OCR_LOCATIONS_IFEC
    elif typeID == 1:
        OCR_LOCATIONS = OCR_LOCATIONS_IFED
    elif typeID == 2:
        OCR_LOCATIONS = OCR_LOCATIONS_INEEF
    elif typeID == 3:
        OCR_LOCATIONS = OCR_LOCATIONS_INEGH

    parsingResults = []
    # loop over the locations of the document we are going to OCR
    for loc in OCR_LOCATIONS:

        # Extract the OCR ROI from the aligned image
        (x, y, w, h) = loc.bbox
        roi = aligned[y:y + h, x:x + w]

        # OCR the ROI using Tesseract
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

        rgb = imutils.resize(rgb, height=150)
        rgb2 = set_image_dpi(rgb)
        temp = cv2.imread(rgb2)
        text = pytesseract.image_to_string(temp)

        # Split every lecture in lines
        for line in text.split("\n"):
            if len(line) <= 2:
                if loc.id == "Nombre" and firstLineName == False:
                    continue
                if loc.id == "Domicilio" and firstLineAddress == False:
                    continue
                if loc.id == "Clave de elector" and firstLineKey == False:
                    continue
                if loc.id == "CURP" and firstLineCURP == False:
                    continue
                if loc.id == "Año de registro" and firstLineYear == False:
                    continue
                if loc.id == "Fecha de nacimiento" and firstLineBirthday == False:
                    continue

            count = sum([line.count(x) for x in loc.filter_keywords])

            # Detect each segment and clean it
            if count == 0:
                if loc.id == 'Nombre':
                    clean = dl.cleanup_Capitals(line)
                    line = clean
                    firstLineName = False
                elif loc.id == "Domicilio":
                    clean = dl.cleanup_AddressValues(line)
                    line = clean
                    firstLineAddress = False
                elif loc.id == 'Clave de elector':
                    words = line.split(" ")
                    line = ""
                    for i in words:
                        if len(i) > 8:
                            clean = dl.cleanup_CapitalsAndNumbers(i)
                            if len(clean) == 18:
                                clean = dl.cleanup_Key(clean)
                                birthKey = getBirthdayFromKey(clean)
                            line = clean
                    firstLineKey = False
                elif loc.id == 'CURP':
                    words = line.split(" ")
                    line = ""
                    for i in words:
                        if len(i) > 5:
                            clean = dl.cleanup_CapitalsAndNumbers(i)
                            if len(clean) == 18:
                                clean = dl.cleanup_CURP(clean)
                                birthCURP = getBirthdayFromCURP(clean)
                            line = clean
                    firstLineCURP = False
                elif loc.id == 'Año de registro':
                    words = line.split(" ")
                    newLine = ""
                    for i in words:
                    	if len(i) == 4:
                    		newLine = i
                    	if len(i) == 2:
                    		newLine = newLine + " " + i
                    	clean = dl.cleanup_Numbers(newLine)
                    	line = clean
                    firstLineYear = False
                elif loc.id == 'Fecha de nacimiento':
                    clean = dl.cleanup_DateValues(line)
                    clean = birthdayConsolidation(clean, birthCURP, birthKey)
                    line = clean
                    firstLineBirthday = False

                parsingResults.append((loc, line))

    results = {}

    # Get strings from OCR results
    for (loc, line) in parsingResults:
    	r = results.get(loc.id, None)
    	if r is None:
    		results[loc.id] = (line, loc._asdict())
    	else:
    		(existingText, loc) = r
    		text = "{}\n{}".format(existingText, line)
    		results[loc["id"]] = (text, loc)

    finalResults= []
    for (locID, result) in results.items():
        (text, loc) = result
        finalResults.append(text)

    return finalResults

def alignDocFunctionGamma(image, template, gamma, typeID):

    OCRLocation = namedtuple("OCRLocation", ["id", "bbox",
    	"filter_keywords"])
    OCR_LOCATIONS = []

    birthCURP = ''
    birthKey = ''
    firstBirthday = ''
    firstLineName = True
    firstLineAddress = True
    firstLineKey = True
    firstLineCURP = True
    firstLineYear = True
    firstLineBirthday = True

    # Adjust light in image
    adjusted = gf.adjustGamma(image, gamma)

    # Align input image to template
    aligned = align_images.align_images(adjusted, template, debug=True)

    aligned = imutils.resize(aligned, width=700)
    alignedHeight, alignedWidth, c = aligned.shape
    image = imutils.resize(image, height = alignedHeight)
    template = imutils.resize(template, width=700)

    # Update OCR Locations according the type of document
    if typeID == 0:
        OCR_LOCATIONS = OCR_LOCATIONS_IFEC
        print("Locations: IFEC")
    elif typeID == 1:
        OCR_LOCATIONS = OCR_LOCATIONS_IFED
        print("Locations: IFED")
    elif typeID == 2:
        OCR_LOCATIONS = OCR_LOCATIONS_INEEF
        print("Locations: INEEF")
    elif typeID == 3:
        OCR_LOCATIONS = OCR_LOCATIONS_INEGH
        print("Locations: INEGH")

    parsingResults = []
    # loop over the locations of the document we are going to OCR
    for loc in OCR_LOCATIONS:

        # Extract the OCR ROI from the aligned image
        (x, y, w, h) = loc.bbox
        roi = aligned[y:y + h, x:x + w]

        # OCR the ROI using Tesseract
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

        rgb = imutils.resize(rgb, height=150)
        rgb2 = set_image_dpi(rgb)
        temp = cv2.imread(rgb2)
        text = pytesseract.image_to_string(temp)

        # Split every lecture in lines

        for line in text.split("\n"):
            if len(line) <= 2:
                if loc.id == "Nombre" and firstLineName == False:
                    continue
                if loc.id == "Domicilio" and firstLineAddress == False:
                    continue
                if loc.id == "Clave de elector" and firstLineKey == False:
                    continue
                if loc.id == "CURP" and firstLineCURP == False:
                    continue
                if loc.id == "Año de registro" and firstLineYear == False:
                    continue
                if loc.id == "Fecha de nacimiento" and firstLineBirthday == False:
                    continue

            count = sum([line.count(x) for x in loc.filter_keywords])

            # Detect each segment and clean it
            if count == 0:
                if loc.id == 'Nombre':
                    clean = dl.cleanup_Capitals(line)
                    line = clean
                    firstLineName = False
                elif loc.id == "Domicilio":
                    clean = dl.cleanup_AddressValues(line)
                    line = clean
                    firstLineAddress = False
                elif loc.id == 'Clave de elector':
                    words = line.split(" ")
                    line = ""
                    for i in words:
                        if len(i) > 8:
                            clean = dl.cleanup_CapitalsAndNumbers(i)
                            if len(clean) == 18:
                                clean = dl.cleanup_Key(clean)
                                birthKey = getBirthdayFromKey(clean)
                            line = clean
                    firstLineKey = False
                elif loc.id == 'CURP':
                    words = line.split(" ")
                    line = ""
                    for i in words:
                        if len(i) > 5:
                            clean = dl.cleanup_CapitalsAndNumbers(i)
                            if len(clean) == 18:
                                clean = dl.cleanup_CURP(clean)
                                birthCURP = getBirthdayFromCURP(clean)
                            line = clean
                    firstLineCURP = False
                elif loc.id == 'Año de registro':
                    words = line.split(" ")
                    newLine = ""
                    for i in words:
                        if len(i) == 4:
                            newLine = i
                        if len(i) == 2:
                            newLine = newLine + " " + i
                        clean = dl.cleanup_Numbers(newLine)
                        line = clean
                    firstLineYear = False
                elif loc.id == 'Fecha de nacimiento':
                    clean = dl.cleanup_DateValues(line)
                    clean = birthdayConsolidation(clean, birthCURP, birthKey)
                    line = clean
                    if firstLineBirthday == True:
                        firstBirthday = clean
                    elif clean == firstBirthday:
                        continue
                    firstLineBirthday = False

                parsingResults.append((loc, line))

    results = {}

    # Get strings from OCR results
    for (loc, line) in parsingResults:
        r = results.get(loc.id, None)
        if r is None:
            results[loc.id] = (line, loc._asdict())
        else:
            (existingText, loc) = r
            text = "{}\n{}".format(existingText, line)
            results[loc["id"]] = (text, loc)

    finalResults= []
    for (locID, result) in results.items():
        (text, loc) = result
        finalResults.append(text)

    return finalResults, adjusted

def cleanup_text(text):
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()

def set_image_dpi(image):
	# Rescaling image to 300dpi without resizing
	tempH, tempW, c = image.shape
	image_resize = im.fromarray(image)
	temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
	temp_filename = temp_file.name
	image_resize.save(temp_filename, dpi=(600, 600))

	return temp_filename

def getBirthdayFromCURP(text):
    year = text[4:6]
    if int(year) > 21:
        year = "19" + year
    else:
        year = "20" + year
    birthday = text[8:10] + '/' + str(text[6:8]) + '/' + year
    return birthday

def getBirthdayFromKey(text):
    year = text[6:8]
    if int(year) > 21:
        year = "19" + year
    else:
        year = "20" + year
    birthday = text[10:12] + '/' + str(text[8:10]) + '/' + year
    return birthday

def birthdayConsolidation(line, curp, key):

    longest = len(line)
    finalBirthday = line
    if len(curp) > longest:
        longest = len(curp)
        finalBirthday = curp
    if len(key) > longest:
        longest = len(key)
        finalBirthday = key

    if finalBirthday != "":
        finalBirthday = validateBirthday(finalBirthday)
    if finalBirthday == "":
        finalBirthday = curp

    return finalBirthday

def validateBirthday(birthday):
    date = birthday.split("/")
    validatedBirthday = ""

    if int(date[0]) > 32 or int(date[0]) < 1:
        print("error de día")
        return validatedBirthday
    elif int(date[1]) > 12:
        print("error de mes")
        return validatedBirthday
    else:
        validatedBirthday = birthday


    return validatedBirthday
