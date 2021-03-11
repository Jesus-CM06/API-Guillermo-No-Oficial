import numpy as np
import imutils
import cv2

def imageOrientation(image):

    turns = 0
    # Resize on the longest side
    height, width, c = image.shape
    if height > width:
    	img = imutils.resize(image, height=500)
    else:
    	img = imutils.resize(image, width=500)

    # Original position
    faces = faceSearch(img)

    if faces > 0:
        return turns #cambiar por la imagen corregida
    else:
        img90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        turns += 1

    # turned 90 degrees
    faces = faceSearch(img90)

    if faces > 0:
        return turns #cambiar por la imagen corregida
    else:
        img180 = cv2.rotate(img90, cv2.ROTATE_90_CLOCKWISE)
        turns += 1

    # turned 180 degrees
    faces = faceSearch(img180)

    if faces > 0:
        return turns #cambiar por la imagen corregida
    else:
        img270 = cv2.rotate(img180, cv2.ROTATE_90_CLOCKWISE)
        turns += 1

    # turned 270 degrees
    faces = faceSearch(img270)

    if faces > 0:
        return turns #cambiar por la imagen corregida
    else:
        print('No faces detected')
        turns += 1

    return turns

def faceSearch(image):

    # Load our serialized model from disk
    prototxtFile = 'Functions/deploy.prototxt'
    modelFile = 'Functions/res10_300x300_ssd_iter_140000.caffemodel'
    
    confidenceParameter = 0.5
    net = cv2.dnn.readNetFromCaffe(prototxtFile, modelFile)

    # Load image and create the blob
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))

    # Pass the blob through the network
    net.setInput(blob)
    detections = net.forward()

    faces = 0

    # loop over the detections
    for i in range(0, detections.shape[2]):
    	# Extract the confidence
        confidence = detections[0, 0, i, 2]

        # Filter results
        if confidence > confidenceParameter:
            faces += 1

    return faces
