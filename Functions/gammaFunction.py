from __future__ import print_function
import numpy as np
import cv2
import Functions.align_images as align_images
import Functions.orientationFunctions as of
import imutils

def gammaFunctionIteration(original, template):

    values = [0.4, 0.6, 0.7, 0.8, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
    bestValues = []
    print("Light adjustment...")
    for gamma in values:

        gamma = gamma if gamma > 0 else 0.1
        adjusted = adjustGamma(original, gamma=gamma)

        aligned = align_images.align_images(adjusted, template, debug=True)

        validate = of.faceSearch(aligned)
        if validate > 0:
            bestValues.append(gamma)

    return bestValues


def gammaFunctionIteration2(original): ###

    # Loop over various values of gamma
    values = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

    for gamma in values:
    	print('Gamma = ' + str(gamma))
    	# Ignore when gamma is 1 (there will be no change to the image)
    	if gamma == 1:
    		continue

    	# Apply gamma correction
    	gamma = gamma if gamma > 0 else 0.1
    	adjusted = adjustGamma(original, gamma=gamma)

    	cv2.putText(adjusted, "g={}".format(gamma), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    	cv2.imshow("Gamma = " + str(gamma), adjusted)

    return

def adjustGamma(image, gamma=1.0):
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")

	return cv2.LUT(image, table)

def ligthIteration(original, template):

    values = [0.6, 1.0, 1.4, 2.0]
    bestValues = []

    for gamma in values:
        gamma = gamma if gamma > 0 else 0.1
        if gamma == 1:
            adjusted = original
        else:
            adjusted = adjustGamma(original, gamma=gamma)

        aligned = align_images.align_images(adjusted, template, debug=True)

        validate = of.faceSearch(aligned)
        if validate > 0:
            bestValues.append(gamma)

    return bestValues
