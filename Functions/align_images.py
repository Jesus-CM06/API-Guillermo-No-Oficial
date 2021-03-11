import numpy as np
import imutils
import cv2

def align_images(image, template, maxFeatures=500, keepPercent=0.2,	debug=False):
	# Convert image and template to grayscale
	imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

	# Detect keypoints
	orb = cv2.ORB_create(maxFeatures)
	(kpsA, descsA) = orb.detectAndCompute(imageGray, None)
	(kpsB, descsB) = orb.detectAndCompute(templateGray, None)

	# Match the features
	method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
	matcher = cv2.DescriptorMatcher_create(method)
	matches = matcher.match(descsA, descsB, None)
	matches = sorted(matches, key=lambda x:x.distance)

	# Keep only the top matches
	keep = int(len(matches) * keepPercent)
	matches = matches[:keep]
	ptsA = np.zeros((len(matches), 2), dtype="float")
	ptsB = np.zeros((len(matches), 2), dtype="float")

	# Check the top matches
	for (i, m) in enumerate(matches):
		ptsA[i] = kpsA[m.queryIdx].pt
		ptsB[i] = kpsB[m.trainIdx].pt

	# Compute homography
	(H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
	# Use the homography matrix to align the images
	(h, w) = template.shape[:2]
	aligned = cv2.warpPerspective(image, H, (w, h))
	return aligned
