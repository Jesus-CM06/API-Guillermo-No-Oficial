import numpy as np
import imutils
import pytesseract
import cv2
import statistics as st
import math
import Functions.delimitadores as dl
import Functions.gammaFunction as gf
from imutils import contours

def backIDRead(image, processWidth=550):

    # Kernels
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))

    # Filters
    image = imutils.resize(image, width=processWidth)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)

    gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")

    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
    thresh = cv2.erode(thresh, None, iterations=4)

    p = int(image.shape[1] * 0.05)
    thresh[:, 0:p] = 0
    thresh[:, image.shape[1] - p:] = 0

    # Finding contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # Analyzing each ROI
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        crWidth = w / float(gray.shape[1])

        pX = int((x + w) * 0.03)
        pY = int((y + h) * 0.03)
        (x, y) = (x - pX, y - pY)
        (w, h) = (w + (pX * 2), h + (pY * 2))
        if x <= 4:
            x = 5
        if y <= 4:
            y = 5

        testRoi = image[y-5 : y+h+10, x-5 : x+w+10].copy()
        roiText = pytesseract.image_to_string(testRoi)
        cleanText = dl.cleanup_BackID(roiText)

        validation = validate(cleanText)

        if validation == False:
            # Flip ROI
            testRoi = cv2.rotate(testRoi, cv2.ROTATE_180)
            # Read ROI
            roiText = pytesseract.image_to_string(testRoi)
            # Clean response
            cleanText = dl.cleanup_BackID(roiText)
            validation = validate(cleanText)

        if validation == True:
            if len(cleanText) > 20:
                roi = testRoi
                cv2.rectangle(image, (x-5, y-5), (x + w + 10, y + h+10), (0, 255, 0), 2)

    # Read and clean the ROI
    roiText = pytesseract.image_to_string(roi)
    cleanText = dl.cleanup_BackID(roiText)

    if len(cleanText) == 30:
        cleanText = dl.cleanup_stringBackID(cleanText)

    backIDStrings = []
    backIDStringsLength = []

    values = [0.4, 0.6, 0.8, 1.0, 2.0, 2.5, 3.0, 3.5]

    # Light testing
    for gamma in values:
    	adjusted = gf.adjustGamma(roi, gamma)

        # Read and clean
    	roiText = pytesseract.image_to_string(adjusted)
    	cleanText = dl.cleanup_BackID(roiText)

        # Validate structure
    	validation = validate(cleanText)

        # Flip
    	if validation == False:
    		roi = cv2.rotate(roi, cv2.ROTATE_180)
    		roiText = pytesseract.image_to_string(roi)
    		cleanText = dl.cleanup_BackID(roiText)

    	divided = cleanText.split(chr(10))

    	backIDStrings.append(divided[0])
    	backIDStringsLength.append((len(divided[0])))

    validation = validate(cleanText)

    if validation == False:
    	roi = cv2.rotate(roi, cv2.ROTATE_180)
    	roiText = pytesseract.image_to_string(roi)
    	cleanText = dl.cleanup_BackID(roiText)

    divided = cleanText.split(chr(10))
    backIDStrings.append(divided[0])
    backIDStringsLength.append((len(divided[0])))

    finalString = consolidateStrings(backIDStrings, backIDStringsLength)

    signIndex = 0
    signIndex = finalString.index("<<")

    cicBegin = signIndex - 10
    if cicBegin < 0:
        cicBegin = 0

    cicEnd = signIndex - 1

    citizenIDBegin = signIndex + 6
    citizenIDEnd = len(finalString)
    cicString = ""
    try:
        cicString = finalString [ cicBegin : cicEnd ]
    except:
        cicString = ""

    try:
        citizenString = finalString [ citizenIDBegin : citizenIDEnd ]
    except:
        cicString = ""


    print("")
    print("final: " + str(finalString))
    print("length: " + str(len(finalString)))
    print("")
    print("CIC: " + str(cicString))
    print("Citizen ID: " + str(citizenString))

    data = {'completeString':finalString, 'CIC':cicString, 'citizenID':citizenString}

    return data

def validate(text):
	if len(text)<5:
		return False

    # Validate the complete string
	validation = False
	sum = 0
	if text[0] == "I":
		sum += 1
	if text[1] == "D":
		sum += 1
	if text[2] == "M":
		sum += 1
	if text[3] == "E":
		sum += 1
	if text[4] == "X":
		sum += 1

    # Validate as substring
	if sum >= 3:
		validation = True
	else:
		subString = text[0:3]
		subString2 = text[0:2]
		if subString in "IDMEX":
			validation = True
		elif subString2 in "IDMEX":
			validation = True
		elif "<<" in text:
			validation = True

	return validation

def consolidateStrings(backIDStrings, backIDStringsLength):
    # Only for the first line
    strings30chars = []
    bool30chars = False
    sameString = True

    # 30 chars?
    for i in range(len(backIDStringsLength)):
        if backIDStringsLength[i] == 30:
            strings30chars.append(backIDStrings[i])
            bool30chars = True

    # Same string?
    if bool30chars == True:
        for i in range(len(strings30chars)-1):
            if strings30chars[i] != strings30chars[i+1]:
                sameString = False
        if sameString == True:
            return strings30chars[0]
        else:
            # Compare format
            finalString = INEformat(strings30chars)
            return finalString
    else:
        # Get the longest string
        longestString = backIDStrings[0] ###
        for i in range(len(backIDStringsLength)-1):
            if backIDStringsLength[i+1] > len(longestString):
                longestString = backIDStrings[i+1]
        return longestString
    return

def INEformat(stringsInFormat):
    correctStrings = []
    sameString = True

    for i in range(len(stringsInFormat)):
        validation = validate(stringsInFormat[1])
        if validation == True:
            correctStrings.append(stringsInFormat[i])

    # Same strings
    if len(correctStrings) == 1:
        return correctStrings[0]

    if len(correctStrings) > 1:
        for i in range(len(correctStrings)-1):
            if correctStrings[i] != correctStrings[i+1]:
                sameString = False
        if sameString == True:
            return correctStrings[0]
        else:
            finalString = INEVote(correctStrings)
            return finalString

    return

def INEVote(correctStrings):
    difStrings = []

    #find different strings
    difStrings.append(correctStrings[0])
    for i in range(len(correctStrings)-1):
        if correctStrings[i+1] != correctStrings[i]:
            difStrings.append(correctStrings[i+1])

    votes = np.zeros(len(difStrings), dtype=int)

    for i in range(len(difStrings)):
        for j in range(len(correctStrings)):
            if correctStrings[j] == difStrings[i]:
                votes[i] += 1
    x = max(votes)

    for i in range(len(votes)):
        if votes[i] == x:
            finalString = difStrings[i]

    return finalString


def backIDReadTypeC(image):
    # Load digits reference and extract digits
    ref = cv2.imread('Functions/digitsReference.jpg')
    digits = extractDigitsFromReference(ref)

    # Resize and convert it to grayscale
    tempImage, gray = imageAdjust(image)

    rotations = 0
    output= []
    while rotations < 4:
    	# ROI detection
        roi = roiDetection(gray)

        if bool(roi) == False:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            tempImage, gray = imageAdjust(image)
            rotations += 1
        else:
            # Digits location and evaluation
            output = blobsDetection(gray, roi, digits)

            if len(output) < 6:
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                tempImage, gray = imageAdjust(image)
                rotations += 1
            else:
                rotations = 4

    data = ""
    data = data.join(output)

    print('')
    print('final: ' + str(data))
    print('length: ' + str(len(data)))

    return data

def extractDigitsFromReference(ref):
	ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
	ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]

	# find contours in reference
	refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	refCnts = imutils.grab_contours(refCnts)
	refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
	digits = {}

	# loop over the reference contours
	for (i, c) in enumerate(refCnts):
		(x, y, w, h) = cv2.boundingRect(c)
		roi = ref[y:y + h, x:x + w]
		roi = cv2.resize(roi, (57, 88))
		digits[i] = roi

	return digits

def imageAdjust(image):
    h, w, d = image.shape
    if h > w:
    	image = imutils.resize(image, width=300)
    else:
    	image = imutils.resize(image, width=750)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, gray

def roiDetection(gray):
    # Kernels
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    # Filters
    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)

    gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,
    	ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
    gradX = gradX.astype("uint8")

    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Find contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    locs = []

    # Loop over the contours
    for (i, c) in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(c)

        # Contours ratio
        ar = w / float(h)
        if ar > 5.0 and ar < 12.0 and w > 90:
            locs.append((x-5, y-5, w+15, h+15))

    return locs

def blobsDetection(gray, locs, digits):
    # Filter blobs by width, height and ratio
    group, digitCnts = firstBlobsFilter(gray, locs)
    # Analyse blobs position
    xString, yString, hString, wString = positionAnalysis(digitCnts)
    # Filter blobs by their poisition
    finalBlobs = secondBlobsFilter(xString, yString, hString, wString)
    # Evaluate each blob
    output = blobsEvaluation(group, finalBlobs, digits)

    return output

def firstBlobsFilter(gray, locs):
    # ROI analysis
    for (i, (gX, gY, gW, gH)) in enumerate(locs):
        # Blob detection
        group = gray[gY:gY + gH, gX:gX + gW]
        group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # Contours detection
        digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        digitCnts = imutils.grab_contours(digitCnts)
        digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]

    return group, digitCnts

def positionAnalysis(digitCnts):
    # Position strings
    xString = []
    yString = []
    hString = []
    wString = []

    # Check each digit
    for c in digitCnts:

        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        if h >= 10 and h < 18:
            if w >= 6 and w < 12:
                if ar >= 0.5 and ar < 0.9:
                    xString.append(x)
                    yString.append(y)
                    hString.append(h)
                    wString.append(w)


    return xString, yString, hString, wString

def secondBlobsFilter(xString, yString, hString, wString):
    xDif = []

    if len(xString) < 2:
    	return xDif

    # X and Y Processing
    yMedian = int(st.median(yString))
    yStdDev = int(math.ceil(st.stdev(yString))+2)

    for i in range(len(xString)-1):
    	xDif.append(xString[i+1] - xString[i])

    xMedian = int(st.median(xDif))
    xStdDev = int(math.ceil(st.stdev(xDif)))
    xDif.insert(0,xMedian)

    # Filters
    finalBlobs = []
    for i in range(len(xDif)):
    	xTest = xDif[i]
    	yTest = yString[i]

    	if xTest >= (xMedian - xStdDev) and xTest <= (xMedian + xStdDev):
    		if yTest >= (yMedian - yStdDev) and yTest <= (yMedian + yStdDev):
    			finalBlobs.append([xString[i], yString[i], wString[i], hString[i]])

    return finalBlobs

def blobsEvaluation(group, finalBlobs, digits):

    # Possible digits results
    output = []

    for element in finalBlobs:
        # Extract a digit a resize it to match templates
        roi = group[ element[1] : element[1] + element[3] , element[0] : element[0] + element[2]]
        roi = cv2.resize(roi, (57, 88))

        scores = []

        # Compare with the reference digits
        for (digit, digitROI) in digits.items():
            result = cv2.matchTemplate(roi, digitROI,cv2.TM_CCOEFF)
            (_, score, _, _) = cv2.minMaxLoc(result)
            scores.append(score)

        # Save the best score
        output.append(str(np.argmax(scores)))

    return output
