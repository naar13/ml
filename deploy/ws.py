
from  __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'model/_Modelo_1.h5'

# Load your trained model
model = load_model(MODEL_PATH)
model._make_predict_function()          # Necessary
# print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
#from keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('')
print('Model loaded. Check http://127.0.0.1:5000/')

'''modelo = 'c:/_Modelo_1.h5'
pesos_modelo = 'c:/_Pesos_1.h5'
cnn = load_model(modelo)'''
model.load_weights("model/_Pesos_1.h5")
res=[]
del(res[:])
def model_predict(file_path):
    
    print(file_path)
    x = load_img(file_path, target_size=(128, 128))
    x = img_to_array(x)
    
    x = np.expand_dims(x, axis=0)

    array = model.predict(x)
    result = array[0]
    answer = np.argmax(result)
    if answer == 0:
        res.append('velocidad minima 30km')
    elif answer == 1:
        res.append('velocidad minima 40km')
  
    elif answer == 2:
        res.append('velocidad minima 60km')
    elif answer == 3:
        res.append('pare')
    elif answer == 4:
        res.append('no parquear')



    


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        model_predict(file_path)
        print(file_path)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
           # ImageNet Decode
                     # Convert to string
        return str(res)

    return None


if __name__ == '__main__':
    app.run(debug=True)