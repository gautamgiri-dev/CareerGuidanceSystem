from flask import Flask, jsonify, request, Response, render_template
import json
from waitress import serve
import pickle
import pandas as pd
import numpy as np
import random
from sklearn import decomposition
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import Normalizer
import warnings
warnings.filterwarnings("ignore")
""" 
Models trained:
    1. Decision Tree Classifier => 3.2%
    2. Decision Tree Classifier Entropy => 3.1%
    3. SVM => 5.75 (Best)
    4. xgboost => 4.41%
    5. KNN => 3.2%
    6. Random Forest Classifier => 2.9%
"""

# Preprocessing data


def preprocess(data):
    # Converting categorical data to numerical data
    label_encoder = LabelEncoder()
    for i in range(14, 38):
        data[:, i] = label_encoder.fit_transform(data[:, i])
    data1 = data[:, :14]
    normalized_data = Normalizer().fit_transform(data1)
    data2 = data[:, 14:]
    df1 = np.append(normalized_data, data2, axis=1)
    return df1


def model_predict(model, data):
    return model.predict(data)


models = ['dtc', 'ent_dtc', 'knn', 'rfc', 'svm']
names = ['Decision Tree Classifier', 'Decition Tree Classifier Entropy',
         'KNN', 'Random Forest Classifier', 'SVM']
loaded_models = []
for model in models:
    model = pickle.load(open(f'./models/{model}.pkl', 'rb'))
    loaded_models.append(model)


app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)['data']
    data = np.array(data).reshape((1, 38))
    data = preprocess(data)
    predictions = []
    for model in loaded_models:
        predictions.append(model_predict(model, data)[0])
    print(predictions)
    return Response(json.dumps(predictions),  mimetype='application/json')


if __name__ == '__main__':
    serve(app)
