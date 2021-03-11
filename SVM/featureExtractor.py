# featureExtractor.py
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from tqdm import tqdm
import numpy as np
import pickle
import os


# Archivo con listas de ejemplos para entrenamiento y pruebas
from TrainingFiles import *

# Carpeta de imágenes para entrenamiento y pruebas
filesDir = "/Volumes/SD128/Proyectos/Xira/XiraDataset/"

# Modelo pre-entrenado
model = VGG16(weights='imagenet', include_top=False)

# Archivos para entrenamiento
trainingLabels = []
trainingClasses = []
embeddings = []
trainingEmbeddings = np.array([])
trainingDelimitations = []

fileNumber = 0
firstClassFile = 0
lastClassFile = 0
lastFile = len(trainingFiles)-1

# Barra de prograso
pbar = tqdm(total=len(trainingFiles))

for file in trainingFiles:
    # Actualiza barra de progreso
    pbar.update(1)
    # Carga una imagen
    img_path = os.path.join(filesDir, file)

    # Si es el primer ejemplo...
    if fileNumber == 0:
        # Agrega la primera clase a la lista
        trainingClasses.append(file.split("_")[0])
        fileNumber += 1
        # Agrega la etiqueta numérica de la clase a la que pertenece
        trainingLabels.append(trainingClasses.index(file.split("_")[0]))

        # Carga y redimensiona la imagen para procesarla con el modelo pre-entrenado
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Obtiene las características en una matriz de 7x7x512 (VGG16)
        features = model.predict(x)
        # Convierte la lista a un arreglo de Numpy
        featuresNumpy = np.array(features)
        # Concatena los valores de la matriz de 7x7x512 y genera un vector de 25088 características
        singleVector = featuresNumpy.flatten()
        # Agrega el vector al listado de ejemplos de entrenamiento
        embeddings.append(singleVector.tolist())

    # Para los siguientes archivos
    else:
        # Revisa si la clase ya existe en el listado de clases. Si no existe, la anexa
        fileClass = file.split("_")[0]
        if fileClass not in trainingClasses:
            trainingClasses.append(fileClass)
            # Como es una clase distinta, agrega el valor de donde termina la clase previa
            lastClassFile = fileNumber-1
            trainingDelimitations.append([firstClassFile, lastClassFile])
            # Guarda la posición del primer ejemplo de la nueva clase
            firstClassFile = fileNumber
        # Agrega la etiqueta numérica de la clase a la que pertenece
        trainingLabels.append(trainingClasses.index(file.split("_")[0]))
        # Carga y redimensiona la imagen para procesarla con el modelo pre-entrenado
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Obtiene las características en una matriz de 7x7x512 (VGG16)
        features = model.predict(x)
        # Convierte la lista a un arreglo de Numpy
        featuresNumpy = np.array(features)
        # Concatena los valores de la matriz de 7x7x512 y genera un vector de 25088 características
        singleVector = featuresNumpy.flatten()
        # Agrega el vector al listado de ejemplos de entrenamiento
        embeddings.append(singleVector.tolist())

        # Si es el último ejemplo...
        if fileNumber == lastFile:
            # Agrega los delimitadores de la última clase
            trainingDelimitations.append([firstClassFile, fileNumber])
        # O continua la cuenta
        else:
            fileNumber += 1

# Convierte la lista de características en un arreglo de Numpy
trainingEmbeddings = np.asarray(embeddings)

# Guarda las características en un archivo CSV
np.savetxt("TrainingFeatures_VGG16_25088.csv", trainingEmbeddings, delimiter=",")



# Archivos para pruebas
testLabels = []
testClasses = []
embeddings = []
testEmbeddings = np.array([])
testDelimitations = []

fileNumber = 0
firstClassFile = 0
lastClassFile = 0
lastFile = len(testFiles)-1

# Barra de prograso
pbar = tqdm(total=len(testFiles))

for file in testFiles:
    # Actualiza barra de progreso
    pbar.update(1)
    if file == '.DS_Store':
        continue
    # Carga una imagen
    img_path = os.path.join(filesDir, file)

    # Si es el primer ejemplo...
    if fileNumber == 0:
        # Agrega la primera clase a la lista
        testClasses.append(file.split("_")[0])
        fileNumber += 1
        # Agrega la etiqueta numérica de la clase a la que pertenece
        testLabels.append(testClasses.index(file.split("_")[0]))

        # Carga y redimensiona la imagen para procesarla con el modelo pre-entrenado
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Obtiene las características en una matriz de 7x7x512 (VGG16)
        features = model.predict(x)
        # Convierte la lista a un arreglo de Numpy
        featuresNumpy = np.array(features)
        # Concatena los valores de la matriz de 7x7x512 y genera un vector de 25088 características
        singleVector = featuresNumpy.flatten()
        # Agrega el vector al listado de ejemplos de entrenamiento
        embeddings.append(singleVector.tolist())

    # Para los siguientes archivos
    else:
        # Revisa si la clase ya existe en el listado de clases. Si no existe, la anexa
        fileClass = file.split("_")[0]
        if fileClass not in testClasses:
            testClasses.append(fileClass)
            # Como es una clase distinta, agrega el valor de donde termina la clase previa
            lastClassFile = fileNumber-1
            testDelimitations.append([firstClassFile, lastClassFile])
            # Guarda la posición del primer ejemplo de la nueva clase
            firstClassFile = fileNumber
        # Agrega la etiqueta numérica de la clase a la que pertenece
        testLabels.append(testClasses.index(file.split("_")[0]))
        # Carga y redimensiona la imagen para procesarla con el modelo pre-entrenado
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Obtiene las características en una matriz de 7x7x512 (VGG16)
        features = model.predict(x)
        # Convierte la lista a un arreglo de Numpy
        featuresNumpy = np.array(features)
        # Concatena los valores de la matriz de 7x7x512 y genera un vector de 25088 características
        singleVector = featuresNumpy.flatten()
        # Agrega el vector al listado de ejemplos de entrenamiento
        embeddings.append(singleVector.tolist())

        # Si es el último ejemplo...
        if fileNumber == lastFile:
            # Agrega los delimitadores de la última clase
            testDelimitations.append([firstClassFile, fileNumber])
        # O continua la cuenta
        else:
            fileNumber += 1

# Convierte la lista de características en un arreglo de Numpy
testEmbeddings = np.asarray(embeddings)

# Estandarización de valores
scaler = StandardScaler()

# Se ajusta con los valores de entrenamiento
scaler.fit(trainingEmbeddings)

# Se aplica el ajuste a ambos conjuntos de características
trainEmbeddings2 = scaler.transform(trainingEmbeddings)
testEmbeddings2 = scaler.transform(testEmbeddings)

# Igualmente, el algoritmo de PCA se ajusta con los nuevos valores de entrenamiento
pca = PCA(.95)
pca.fit(trainEmbeddings2)

# Se aplica el PCA a ambos conjuntos de características
trainPCA = pca.transform(trainEmbeddings2)
testPCA = pca.transform(testEmbeddings2)

# Guarda todas las variables necesarias para un entrenamiento con las 475 características obtenidas del PCA
np.savez("VGG16_PCA_features.npz", trainingFiles=trainingFiles, testFiles=testFiles, trainingLabels=trainingLabels, testLabels=testLabels, trainingClasses=trainingClasses, testClasses=testClasses, trainingDelimitations=trainingDelimitations, testDelimitations=testDelimitations, trainingEmbeddings=trainPCA, testEmbeddings=testPCA)

# Guarda SCALER y PCA (necesarios para procesar cualquier nueva muestra)
pickle.dump(scaler, open('scaler', 'wb'))
pickle.dump(pca, open('pca', 'wb'))
