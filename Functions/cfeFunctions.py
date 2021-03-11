import Functions.align_images as alImg
import numpy as np
import imutils
import cv2
import datetime
from collections import namedtuple
import pytesseract
import Functions.delimitadores as dl

OCRLocation = namedtuple("OCRLocation", ["id", "bbox", "filter_keywords"])

def loadDefaults():
    templates = []
    templates.append(cv2.imread('Templates/templateCFE1.png'))
    templates.append(cv2.imread('Templates/templateCFE2.png'))
    templates.append(cv2.imread('Templates/templateCFE3.png'))
    templates.append(cv2.imread('Templates/templateCFE4.png'))
    templates.append(cv2.imread('Templates/templateCFE5.png'))
    templates.append(cv2.imread('Templates/templateCFE6.png'))
    templates.append(cv2.imread('Templates/templateCFE7.png'))
    templates.append(cv2.imread('Templates/templateCFE8.png'))

    OCR_Locations = []
    OCR_Locations.append(OCRLocation("TEMPLATE1", (5, 120, 305, 130), ["Comision", "Federal", "De", "Electricidad"]))
    OCR_Locations.append(OCRLocation("TEMPLATE2", (25, 92, 239, 78), ["Comision", "Federal", "De", "Electricidad"]))
    OCR_Locations.append(OCRLocation("TEMPLATE3", (10, 110, 313, 97), ["Comision", "Federal", "De", "Electricidad"]))
    OCR_Locations.append(OCRLocation("TEMPLATE4", (63, 184, 519, 187), ["Comision", "Federal", "De", "Electricidad"]))
    OCR_Locations.append(OCRLocation("TEMPLATE5", (13, 115, 317, 110), ["Comision", "Federal", "De", "Electricidad"]))
    OCR_Locations.append(OCRLocation("TEMPLATE6", (10, 68, 332, 88), ["Comision", "Federal", "De", "Electricidad"]))
    OCR_Locations.append(OCRLocation("TEMPLATE7", (14, 60, 611, 215), ["Comision", "Federal", "De", "Electricidad"]))
    OCR_Locations.append(OCRLocation("TEMPLATE8", (27, 59, 519, 211), ["Comision", "Federal", "De", "Electricidad"]))

    return templates, OCR_Locations

def alignToTemplates(image, templates):
    alignedImages = []
    for template in templates:
        aligned = alImg.align_images(image, template, debug=True) ###
        alignedImages.append(imutils.resize(aligned, width=700))
    return alignedImages

def readLocations(alignedImages, OCR_Locations):
    OCR_results = []
    #print('Reading...')

    for i in range(len(alignedImages)):
        loc = OCR_Locations[i]
        (x, y, w, h) = loc.bbox
        roi = alignedImages[i][y:y + h, x:x + w]
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(rgb, height=150)
        text = pytesseract.image_to_string(rgb)

        finalText = ""
        for line in text.split("\n"):
            count = sum([line.count(x) for x in loc.filter_keywords])
            if count == 0:
                line = dl.cleanup_AddressValues(line)
                if len(line) > 2:
                    finalText = finalText + line + "\n"
        OCR_results.append(finalText)

    return OCR_results

def finalResult(OCR_results):
    longestString = ""
    longestStringIndex = 0
    for i in range(len(OCR_results)):
        if len(OCR_results[i]) > len(longestString):
            longestString = OCR_results[i]
            longestStringIndex = i

    return longestString
