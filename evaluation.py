# Evaluation
import pickle

def embeddingEvaluation(embedding):

    # Loading Pickles
    path = 'Pickles/'

    IFEFRCmodel = pickle.load(open(path + 'IFEFRCmodel', 'rb'))
    IFEFRDmodel = pickle.load(open(path + 'IFEFRDmodel', 'rb'))
    INEFREFmodel = pickle.load(open(path + 'INEFREFmodel', 'rb'))
    INEFRGHmodel = pickle.load(open(path + 'INEFRGHmodel', 'rb'))
    IFERECmodel = pickle.load(open(path + 'IFERECmodel', 'rb'))
    IFEREDmodel = pickle.load(open(path + 'IFEREDmodel', 'rb'))
    INEREEFmodel = pickle.load(open(path + 'INEREEFmodel', 'rb'))
    INEREGHmodel = pickle.load(open(path + 'INEREGHmodel', 'rb'))
    LUZmodel = pickle.load(open(path + 'LUZmodel', 'rb'))
    TELMEXmodel = pickle.load(open(path + 'TELMEXmodel', 'rb'))

    testSample = embedding[0:1]
    results = []
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

    bestModel = max(results)

    position = results.index(bestModel)
    label = ''

    if position == 0:
        label = 'IFE Frente C'
        print("IFE Frente C")
    elif position == 1:
        label = 'IFE Frente D'
        print("IFE Frente D")
    elif position == 2:
        label = 'INE Frente EF'
        print("Evaluation: INE Frente EF")
    elif position == 3:
        label = 'INE Frente GH'
        print("INE Frente GH")
    elif position == 4:
        label = 'IFE Reverso C'
        print("IFE Reverso C")
    elif position == 5:
        label = 'INE Reverso D'
        print("INE Reverso D")
    elif position == 6:
        label = 'INE Reverso EF'
        print("INE Reverso EF")
    elif position == 7:
        label = 'INE Reverso GH'
        print("INE Reverso GH")
    elif position == 8:
        label = 'Recibo de Luz'
        print("Recibo de Luz")
    elif position == 9:
        label = 'Recibo de Telmex'
        print("Recibo de Telmex")

    return position, results, label
