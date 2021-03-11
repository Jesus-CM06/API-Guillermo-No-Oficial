import Functions.align_images as alImg
import numpy as np
import imutils
import cv2
import datetime
from collections import namedtuple
import pytesseract
import Functions.delimitadores as dl


OCRLocation = namedtuple("OCRLocation", ["id", "bbox", "filter_keywords"])

def detectOrientation(image):
    box = detectBarCode(image)
    orientation = orderPoints(box)

    return orientation

def detectBarCode(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
    gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    closed = cv2.erode(closed, None, iterations = 4)
    closed = cv2.dilate(closed, None, iterations = 4)

    cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

    rect = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
    box = np.int0(box)

    return box

def orderPoints(box):
    xValues = []
    yValues = []
    for pair in box:
        xValues.append(pair[0])
        yValues.append(pair[1])

    left = []
    rigth = []
    up = []
    down = []

    left.append(min(xValues))
    xValues.remove(min(xValues))
    left.append(min(xValues))
    xValues.remove(min(xValues))
    rigth = xValues

    up.append(min(yValues))
    yValues.remove(min(yValues))
    up.append(min(yValues))
    yValues.remove(min(yValues))
    down = yValues

    if left[0] == left[1] and rigth[0] == rigth[1] and up[0] == up[1] and down[0]==down[1]:
        upleft = [left[0], up[0]]
        downrigth = [rigth[0], down[0]]
        uprigth = [rigth[0], up[0]]
        downleft = [left[0], down[0]]
    else:
        xValues = []
        yValues = []
        for pair in box:
            xValues.append(pair[0])
            yValues.append(pair[1])

        upleft = []
        uprigth = []
        downleft = []
        downright = []

        #upleft
        for i in left:
            leftindex = xValues.index(i)
            for j in up:
                upindex = yValues.index(j)
                if leftindex == upindex:
                    upleft = [i,j]
                    left.remove(i)
                    up.remove(j)
                    break

        #downright
        for i in rigth:
            rigthindex = xValues.index(i)
            for j in down:
                downindex = yValues.index(j)
                if rigthindex == downindex:
                    downrigth = [i,j]
                    rigth.remove(i)
                    down.remove(j)
                    break

        uprigth = [rigth[0], up[0]]
        downleft = [left[0], down[0]]


    ancho = uprigth[0] - upleft[0]
    alto = downleft[1] - upleft[1]

    orientation = True
    if alto >= ancho:
        orientation = False

    return orientation

def loadDefaults():
    templates = []
    templates.append(cv2.imread('Templates/templateTelmex1.png'))
    templates.append(cv2.imread('Templates/templateTelmex2.png'))
    templates.append(cv2.imread('Templates/templateTelmex3.png'))
    templates.append(cv2.imread('Templates/templateTelmex4.png'))
    templates.append(cv2.imread('Templates/templateTelmex5.png'))
    templates.append(cv2.imread('Templates/templateTelmex6.png'))

    OCR_Locations = []
    OCR_Locations.append(OCRLocation("TEMPLATE1", (2, 141, 360, 144), ["TELMEX", "TELEFONOS", "Parque", "Via", "06500", "RFC", "DV", "TME840315-KT6", "KT6"]))
    OCR_Locations.append(OCRLocation("TEMPLATE2", (3, 298, 689, 311), ["TELMEX", "TELEFONOS", "Parque", "Via", "06500", "RFC", "DV", "TME840315-KT6", "KT6"]))
    OCR_Locations.append(OCRLocation("TEMPLATE3", (8, 321, 682, 335), ["TELMEX", "TELEFONOS", "Parque", "Via", "06500", "RFC", "DV", "TME840315-KT6", "KT6"]))
    OCR_Locations.append(OCRLocation("TEMPLATE4", (4, 142, 315, 145), ["TELMEX", "TELEFONOS", "Parque", "Via", "06500", "RFC", "DV", "TME840315-KT6", "KT6"]))
    OCR_Locations.append(OCRLocation("TEMPLATE5", (28, 145, 381, 126), ["TELMEX", "TELEFONOS", "Parque", "Via", "06500", "RFC", "DV", "TME840315-KT6", "KT6"]))
    OCR_Locations.append(OCRLocation("TEMPLATE6", (10, 147, 292, 143), ["TELMEX", "TELEFONOS", "Parque", "Via", "06500", "RFC", "DV", "TME840315-KT6", "KT6"]))

    return templates, OCR_Locations

def alignToTemplates(image, templates):
    alignedImages = []
    for template in templates:
        aligned = alImg.align_images(image, template, debug=True)
        alignedImages.append(imutils.resize(aligned, width=700))
    return alignedImages

def readLocations(alignedImages, OCR_Locations):
    OCR_results = []
    print('Reading...')

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
                if len(line) > 12:
                    finalText = finalText + line + "\n"
        OCR_results.append(finalText)

    return OCR_results

def readFromBarCode(alignedImages, OCR_Location):
    readsFromBarCode = []
    for image in alignedImages:
        try:
            box = detectBarCode(image)
            topLeft, bottomRigth = getNewBox(box)

            roi = image[topLeft[1]:bottomRigth[1], topLeft[0]:bottomRigth[0]]
            rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(rgb, height=150)
            text = pytesseract.image_to_string(rgb)

            loc = OCR_Location
            finalText = ""
            for line in text.split("\n"):
                count = sum([line.count(x) for x in loc.filter_keywords])
                if count == 0:
                    line = dl.cleanup_AddressValues(line)
                    if len(line) > 12:
                        finalText = finalText + line + "\n"
            readsFromBarCode.append(finalText) ###
        except:
            readsFromBarCode.append("")

    return readsFromBarCode

def getNewBox(box):
    xValues = []
    yValues = []
    for pair in box:
        xValues.append(pair[0])
        yValues.append(pair[1])

    left = []
    rigth = []
    up = []
    down = []

    left.append(min(xValues))
    xValues.remove(min(xValues))
    left.append(min(xValues))
    xValues.remove(min(xValues))
    rigth = xValues

    up.append(min(yValues))
    yValues.remove(min(yValues))
    up.append(min(yValues))
    yValues.remove(min(yValues))
    down = yValues

    if left[0] == left[1] and rigth[0] == rigth[1] and up[0] == up[1] and down[0]==down[1]:
        upleft = [left[0], up[0]]
        downrigth = [rigth[0], down[0]]
        uprigth = [rigth[0], up[0]]
        downleft = [left[0], down[0]]
    else:
        xValues = []
        yValues = []
        for pair in box:
            xValues.append(pair[0])
            yValues.append(pair[1])

        upleft = []
        uprigth = []
        downleft = []
        downright = []

        #upleft
        for i in left:
            leftindex = xValues.index(i)
            for j in up:
                upindex = yValues.index(j)
                if leftindex == upindex:
                    upleft = [i,j]
                    left.remove(i)
                    up.remove(j)
                    break

        #downright
        for i in rigth:
            rigthindex = xValues.index(i)
            for j in down:
                downindex = yValues.index(j)
                if rigthindex == downindex:
                    downrigth = [i,j]
                    rigth.remove(i)
                    down.remove(j)
                    break

        uprigth = [rigth[0], up[0]]
        downleft = [left[0], down[0]]


    ancho = uprigth[0] - upleft[0]
    alto = downleft[1] - upleft[1]

    newSquareHeight = round(ancho*.7)
    bestHeigh = max([uprigth[1],upleft[1]])

    topLeft = (upleft[0],upleft[1]-newSquareHeight)
    bottomRigth = (uprigth[0],bestHeigh)

    return topLeft, bottomRigth

def finalResult(OCR_results, reads):
    longestString = ""
    longestStringIndex = 0
    for i in range(len(OCR_results)):
        if len(OCR_results[i]) > len(longestString):
            longestString = OCR_results[i]
            longestStringIndex = i

    for i in range(len(reads)):
        if len(reads[i]) > len(longestString):
            longestString = reads[i]
            longestStringIndex = i


    return longestString
