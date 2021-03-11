# Reading

import Functions.orientationFunctions as of
import Functions.gammaFunction as gf
import Functions.validationFunctions as vf
import Functions.backIDFunctions as bidf
import Functions.alignDocFunctions as adf
import Functions.cfeFunctions as cfe
import Functions.telmexFunctions as telmex
import numpy as np
import cv2
import imutils
from collections import namedtuple

def documentReading(img, typeID):
    data=''
    if typeID == 0:
        print("IFE Frente C")
        data = idFront(img, typeID)
    elif typeID == 1:
        print("IFE Frente D")
        data = idFront(img, typeID)
    elif typeID == 2:
        print("Reading: INE Frente EF")
        data = idFront(img, typeID)
    elif typeID == 3:
        print("INE Frente GH")
        data = idFront(img, typeID)
    elif typeID == 4:
        print("IFE Reverso C")
        data = bidf.backIDReadTypeC(img)
    elif typeID == 5:
        print("INE Reverso D")
        data = bidf.backIDRead(img)
    elif typeID == 6:
        print("INE Reverso EF")
        data = bidf.backIDRead(img)
    elif typeID == 7:
        print("INE Reverso GH")
        data = bidf.backIDRead(img)
    elif typeID == 8:
        print("Recibo de Luz")
        data = cfeReading(img)
    elif typeID == 9:
        print("Recibo de Telmex")
        data = telmexReading(img)

    return data

def idFront(imgCV, typeID):

    # Resize to width = 950
    imgCV = imutils.resize(imgCV, width=950)
    print('Reading: ' + str(imgCV.shape) )

    # Load Template
    if typeID == 0:
        template = cv2.imread('Templates/CTemplate1.png')
    elif typeID == 1:
        template = cv2.imread('Templates/DTemplate1.jpg')
    elif typeID == 2:
        template = cv2.imread('Templates/EFTemplate.png')
    elif typeID == 3:
        template = cv2.imread('Templates/GHTemplate1.png')

    print(template.shape)

    # Best position
    bestPosition = of.imageOrientation(imgCV)

    # Correct Orientation
    for i in range(bestPosition):
        imgCV = cv2.rotate(imgCV, cv2.ROTATE_90_CLOCKWISE)

    # Best Gamma Values
    boolSize = False

    bestGammaValues = gf.gammaFunctionIteration(imgCV, template)
    print(bestGammaValues)
    if len(bestGammaValues) > 6:
        # IMPROVE BY SELECTING FROM RESULTS
    	bestGammaValues = [0.6, 1.0, 1.2, 1.4, 1.6, 2.0]
    print(bestGammaValues)

    # Best Sizes
    if bestGammaValues == []: # TAKE NEW CONSIDERATIONS
    	boolSize = True
    	bestWidthValues = vf.validateSizes(imgCV, template)
    	print(bestWidthValues)

    	if bestWidthValues == []:
    		print("vacía")
    		return 'vacía'

    # READING WITH TEMPLATE! #####
    print("near template...")
    names = []
    address = []
    keys = []
    curps = []
    years = []
    birthdays = []

    if boolSize == False:
        for gamma in bestGammaValues:
            print("Gamma: " + str(gamma))
            final, adjusted = adf.alignDocFunctionGamma(imgCV, template, gamma, typeID)

            names.append(final[0])
            address.append(final[1])
            keys.append(final[2])
            curps.append(final[3])
            years.append(final[4])
            birthdays.append(final[5])

    else:
    	for width in bestWidthValues:
    		print("Width: " + str(width))
    		final = adf.alignDocFunction(imutils.resize(imgCV, width=width), template, typeID)

    		names.append(final[0])
    		address.append(final[1])
    		keys.append(final[2])
    		curps.append(final[3])
    		years.append(final[4])
    		birthdays.append(final[5])

    # Validate String
    bestStrings = vf.validateStrings(names, address, keys, curps, years, birthdays)
    data = {'name':bestStrings[0], 'address':bestStrings[1], 'key':bestStrings[2], 'curp':bestStrings[3], 'year':bestStrings[4], 'birthday':bestStrings[5]}

    print("")
    print("Mejores strings: ")
    print("")
    print(bestStrings[0])
    print(bestStrings[1])
    print(bestStrings[2])
    print(bestStrings[3])
    print(bestStrings[4])
    print(bestStrings[5])

    return data

def cfeReading(img):
    templates, OCR_Locations = cfe.loadDefaults()
    alignedImages = cfe.alignToTemplates(img, templates)
    OCR_results = cfe.readLocations(alignedImages, OCR_Locations)
    data = cfe.finalResult(OCR_results)
    print(data)
    return data

def telmexReading(img):
    orientation = telmex.detectOrientation(img)
    if orientation == False:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    templates, OCR_Locations = telmex.loadDefaults()
    alignedImages = telmex.alignToTemplates(img, templates)
    OCR_results = telmex.readLocations(alignedImages, OCR_Locations)
    reads = telmex.readFromBarCode(alignedImages, OCR_Locations[0])
    data = telmex.finalResult(OCR_results, reads)
    print(data)

    return data
