# Preprocessing

import numpy as np
import pickle
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input

def imagePreprocessing(image):
    # Feature Extraction
    newEmbedding = featureExtraction(image)

    # Scaler and PCA
    finalEmbedding = scalerAndPCA(newEmbedding)

    return finalEmbedding

def featureExtraction(img):
    model = VGG16(weights='imagenet', include_top=False)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    featuresNumpy = np.array(features)
    singleVector = featuresNumpy.flatten()
    newEmbedding = singleVector.tolist()
    return newEmbedding

def scalerAndPCA(newEmbedding):
    path = "Pickles/"
    # SCALER AND PCA
    scaler = pickle.load(open(path + 'scaler', 'rb'))
    pca = pickle.load(open(path + 'pca', 'rb'))

    loadeddata = np.load(path + 'Features.npz')
    testEmbeddings = loadeddata["testEmbeddings"]

    testDummy = []
    testDummy.append(newEmbedding)
    testDummy.append(testEmbeddings[0].tolist())
    test = np.asarray(testDummy)

    scaledTest = scaler.transform(test)
    pcaTest = pca.transform(scaledTest)
    return pcaTest
