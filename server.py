#!/anaconda3/envs/flask_api/bin/python
from flask import Flask, request, jsonify
import joblib
import pandas as pd 
import json
import numpy as np

app = Flask(__name__)
# Load the model from the file 
model = joblib.load('models/final_model.pkl')


@app.route('/predict',methods=['POST'])

def predict():
    # Get the data from the POST request.
    # curl "localhost:5000/predict" -H "Content-Type: application/json" -d "{\"message\": \"I feel like drinking\" }"
    data = request.get_json(force=True)
    final = data[0]
    #final = pd.DataFrame.from_dict(data,orient='index')
    prediction = model.predict(list(final))
    #output = prediction[0]    
    #return jsonify(output)
    return jsonify(prediction[0])
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)
