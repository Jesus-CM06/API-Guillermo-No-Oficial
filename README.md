Xira project colaboration for information extraction using OCR, Image Processing, Computer Vision, Patern Recognition and Classificators techniques.

(Open to watch clearly the project structure)

Project Structure

idReader.py [API]
|
├─── preprocessing.py
├─── evaluation.py
├─── reading.py
|
├─────  Functions
|       ├───  __init__.py
|       ├───  align_images.py
|       ├───  alignDocFunctions.py
|       ├───  backIDFunctinos.py
|       ├───  cfeFunctinos.py
|       ├───  delimitadores.py
|       ├───  gammaFunctions.py
|       ├───  OCRLocations.py
|       ├───  orientationFunctions.py
|       ├───  telmexFunctions.py
|       ├───  validationsFunctions.py
|       ├───  deploy.prototxt
|       ├───  res10_300x300_ssd_iter_140000.caffemodel
|       └───  digitsReference.jpg
|
├─────  Pickles
|       ├───  pca           (on GoogleDrive due to size limits)
|       ├───  Features.npz  (on GoogleDrive due to size limits)
|       ├───  README.md
|       ├───  scaler
|       ├───  IFEFRCmodel
|       ├───  IFEFRDmodel
|       ├───  INEFREFmodel
|       ├───  INEFRGHmodel
|       ├───  IFERECmodel
|       ├───  IFEREDmodel
|       ├───  INEREEFmodel
|       ├───  INEREGHmodel
|       ├───  LUZmodel
|       └───  TELMEXmodel
|       
├─────  Templates
|       ├───  CTemplate1.png
|       ├───  DTemplate1.png
|       ├───  EFTemplate1.png
|       ├───  GHTemplate1.png
|       ├───  templateCFE1.png
|       ├───  templateCFE2.png
|       ├───  templateCFE3.png
|       ├───  templateCFE4.png
|       ├───  templateCFE5.png
|       ├───  templateCFE6.png
|       ├───  templateCFE7.png
|       ├───  templateCFE8.png
|       ├───  templateTelmex1.png
|       ├───  templateTelmex2.png
|       ├───  templateTelmex3.png
|       ├───  templateTelmex4.png
|       ├───  templateTelmex5.png
|       └───  templateTelmex6.png
|       
├─────  SVM
|       ├───  Manual de entrenamiento de SVM.pdf
|       ├───  TrainingFiles.py
|       ├───  featureExtractor.py
|       └───  trainingSVM.py
|
└─────  Examples
        └───  (Several images to test the API)
