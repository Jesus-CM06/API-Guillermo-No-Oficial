# trainingSVM
from sklearn.svm import SVC
import numpy as np
import pickle

# Archivo con las variables para el entrenamiento
datasetFile = "VGG16_PCA_475features.npz"

# Cargar archivo y asignar variables
loadeddata = np.load(datasetFile)
trainingFiles = loadeddata["trainingFiles"]
testFiles = loadeddata["testFiles"]
trainingLabels = loadeddata["trainingLabels"]
testLabels = loadeddata["testLabels"]
trainingClasses = loadeddata["trainingClasses"]
testClasses = loadeddata["testClasses"]
trainingDelimitations = loadeddata["trainingDelimitations"]
testDelimitations = loadeddata["testDelimitations"]
trainingEmbeddings = loadeddata["trainingEmbeddings"]
testEmbeddings = loadeddata["testEmbeddings"]

# Se entrenan tantos modelos como clases se tengan, la SVM utiliza un enfoque One vs All
for targetClass in range(len(trainingClasses)):

    yTrain = []
    # Se obtienen los límites de la clase a entrenar (que archivos comprenden esta clase)
    lowBoundry = trainingDelimitations[targetClass, 0]
    highBoundry = trainingDelimitations[targetClass, 1]

    # Si el ejemplo pertenece a la clase a entrenar, su etiqueta será 1, caso contrario 0
    for i in range(len(trainingEmbeddings)):
        if i >= lowBoundry and i<= highBoundry:
            yTrain.append(1)
        else:
            yTrain.append(0)

    # Depende del orden de los archivos a entrenar
    if targetClass == 0:
        # Inicializa el modelo con un tipo de kernel y la opción de obtener la probabilidad en decimales.
        IFEFRCmodel = SVC(kernel='linear', probability = True)
        # Se entrena el modelo con las muestras y etiquetas de una determinada clase.
        IFEFRCmodel.fit(trainingEmbeddings, yTrain)
    elif targetClass == 1:
        IFEFRDmodel = SVC(kernel='linear', probability = True)
        IFEFRDmodel.fit(trainingEmbeddings, yTrain)
    elif targetClass == 2:
        INEFREFmodel = SVC(kernel='linear', probability = True)
        INEFREFmodel.fit(trainingEmbeddings, yTrain)
    elif targetClass == 3:
        INEFRGHmodel = SVC(kernel='linear', probability = True)
        INEFRGHmodel.fit(trainingEmbeddings, yTrain)
    elif targetClass == 4:
        IFERECmodel = SVC(kernel='linear', probability = True)
        IFERECmodel.fit(trainingEmbeddings, yTrain)
    elif targetClass == 5:
        IFEREDmodel = SVC(kernel='linear', probability = True)
        IFEREDmodel.fit(trainingEmbeddings, yTrain)
    elif targetClass == 6:
        INEREEFmodel = SVC(kernel='linear', probability = True)
        INEREEFmodel.fit(trainingEmbeddings, yTrain)
    elif targetClass == 7:
        INEREGHmodel = SVC(kernel='linear', probability = True)
        INEREGHmodel.fit(trainingEmbeddings, yTrain)
    elif targetClass == 8:
        LUZmodel = SVC(kernel='linear', probability = True)
        LUZmodel.fit(trainingEmbeddings, yTrain)
    elif targetClass == 9:
        TELMEXmodel = SVC(kernel='linear', probability = True)
        TELMEXmodel.fit(trainingEmbeddings, yTrain)

# Inicialización de la matriz de confusión (depende de las clases que se entrenan)
matResults = np.zeros([len(trainingClasses),len(trainingClasses)], dtype=int)

# Evaluación de las muestras de prueba
for i in range(len(testEmbeddings)):
    testSample = testEmbeddings[i:i+1]
    results = []
    # Evalua la muestra con los modelos creados y se guarda la probabilidad en la variable results
    results.append(float(IFEFRCmodel.decision_function(testSample)))
    results.append(float(IFEFRDmodel.decision_function(testSample)))
    results.append(float(INEFREFmodel.decision_function(testSample)))
    results.append(float(INEFRGHmodel.decision_function(testSample)))
    results.append(float(IFERECmodel.decision_function(testSample)))
    results.append(float(IFEREDmodel.decision_function(testSample)))
    results.append(float(INEREEFmodel.decision_function(testSample)))
    results.append(float(INEREGHmodel.decision_function(testSample)))
    results.append(float(LUZmodel.decision_function(testSample)))
    results.append(float(TELMEXmodel.decision_function(testSample)))

    # Busca el mayor valor en los resultados
    bestModel = max(results)
    # Busca a que modelo pertenece el mejor resultado
    position = results.index(bestModel)
    # Suma 1 punto acorde a la posición de la clase real contra la predicha por los modelos
    matResults[testLabels[i],position] += 1

    # Imprimie la clase predicha para la muestra y la clase real a la que pertenecía
    print("Pred: " + str(position) + " (" + testClasses[position] + "), Real: " + str(testLabels[i]) + " ("
        + testClasses[testLabels[i]] + ")")

# Imprime la matriz de confusión
print(matResults)

pickle.dump(IFEFRCmodel, open('IFEFRCmodel', 'wb'))
pickle.dump(IFEFRDmodel, open('IFEFRDmodel', 'wb'))
pickle.dump(INEFREFmodel, open('INEFREFmodel', 'wb'))
pickle.dump(INEFRGHmodel, open('INEFRGHmodel', 'wb'))
pickle.dump(IFERECmodel, open('IFERECmodel', 'wb'))
pickle.dump(IFEREDmodel, open('IFEREDmodel', 'wb'))
pickle.dump(INEREEFmodel, open('INEREEFmodel', 'wb'))
pickle.dump(INEREGHmodel, open('INEREGHmodel', 'wb'))
pickle.dump(LUZmodel, open('LUZmodel', 'wb'))
pickle.dump(TELMEXmodel, open('TELMEXmodel', 'wb'))
