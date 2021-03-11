# API

from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing import image
import Functions.orientationFunctions as of
import cv2
import tempfile
from PIL import Image as im

import preprocessing as prep
import evaluation as ev
import reading as rd
import os


app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>OCR Xira</h1>"

@app.route('/api/ocr', methods=['GET'])
def api_id():
    results = ''
    if 'id' in request.args:
        id = request.args['id']
        print(id)

        imgCV = cv2.imread(id)
        print(imgCV.shape)

        # Best position
        bestPosition = of.imageOrientation(imgCV)

        # Correct Orientation
        for i in range(bestPosition):
            imgCV = cv2.rotate(imgCV, cv2.ROTATE_90_CLOCKWISE)

        # Temporal File
        image_resize = im.fromarray(imgCV)
        suffix = id.split(".")[-1]
        print(suffix)
        #temp_file = tempfile.NamedTemporaryFile(delete=True, suffix='.'+suffix)
        #temp_filename = temp_file.name
        temp_filename = ("tempImage." + suffix)
        image_resize.save(temp_filename)

        img = image.load_img(temp_filename, target_size=(224,224))
        os.remove(temp_filename)

        # Preprocessing
        print("Preprocessing...") ###
        finalEmbedding = prep.imagePreprocessing(img)

        # Evaluate
        print("Evaluation...") ###
        evaluation, results, label = ev.embeddingEvaluation(finalEmbedding)

        # Reading
        print("Reading...") ###
        data = rd.documentReading(imgCV,evaluation)

        return jsonify(data)
    else:
        return 'empty line'
    return 'empty'

if __name__ == '__main__':
    app.run(debug=False)
