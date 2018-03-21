import os
from flask import Flask, request
import pickle
import numpy as np
import requests
from io import BytesIO
from PIL import Image
from settings import APP_ROOT

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hi"

@app.route("/predict",methods=['POST','GET'])
def predict():
    try:
        # labels
        categories = ['dataset/gear_images/axes', 'dataset/gear_images/boots',
       'dataset/gear_images/carabiners', 'dataset/gear_images/crampons',
       'dataset/gear_images/gloves',
       'dataset/gear_images/hardshell_jackets',
       'dataset/gear_images/harnesses', 'dataset/gear_images/helmets',
       'dataset/gear_images/insulated_jackets',
       'dataset/gear_images/pulleys', 'dataset/gear_images/rope',
       'dataset/gear_images/tents']

        if request.method=='POST':
            imageUrl = request.json['image_url']

            # get the image and create a vector
            response = requests.get(imageUrl)
            img = Image.open(BytesIO(response.content))

            # preprocess image
            size = [128,128]
            thumb = img.copy()
            thumb.thumbnail(size,Image.ANTIALIAS)
            padded_img = Image.new("RGB", size, "white")
            padded_img.paste(thumb, (int((size[0] - thumb.size[0])/2),0))

            # create image vector
            data = np.array(padded_img).flatten()
            data = data.reshape(1,-1)

            #predict
            with open(os.path.join(APP_ROOT, 'YOUR_MODEL_FILE_NAME e.g. trained_model.pkl'), 'rb') as f:
                model = pickle.load(f)
                prediction = model.predict(data)
                return categories[prediction[0]]
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0')