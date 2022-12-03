from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_minify import minify

# import tensorflow as tf
from keras.models import load_model

# from keras.utils import img_to_array
import re

# import pandas as pd
import numpy as np
import base64
import io
from PIL import Image

app = Flask(__name__)
minify(app=app, html=True, js=True, cssless=True)


# define input_size
input_size = (100, 100)
# define labels
labels = ['A', 'Ba', 'Da', 'Ga', 'Ha', 'I', 'Ja', 'Ka', 'La', 'Ma', 'Na', 'Nga', 'Nya', 'Pa', 'Ra', 'Sa', 'Ta', 'U', 'Wa', 'Ya']
labels_rep = ['a', 'b', 'd', 'g', 'k', 'I', 'j', 'k', 'l', 'm', 'n', '<', '[', 'p', 'r', 's', 't', 'U', 'w', 'y']


def predict_fit(image_data):
    MODEL_PATH = "./asima_Model.h5"
    model = load_model(MODEL_PATH, compile=False)
    
    img = base64.b64decode(image_data)
    img = Image.open(io.BytesIO(img))
    # adding bgcolor
    fill_color = (225, 225, 225)  # your new background color
    img = img.convert("RGBA")  # it had mode P after DL it from OP
    if img.mode in ("RGBA", "LA"):
        background = Image.new(img.mode[:-1], img.size, fill_color)
        background.paste(img, img.split()[-1])  # omit transparency
        img = background
    img = img.convert("RGB").resize(input_size, resample=0)

    x = (np.array(img)) / 255  # image2Arr
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    classes = model.predict(images, batch_size=32)

    res1 = labels[np.argmax(classes)]
    res2 = labels_rep[np.argmax(classes)]
    res2 = "(" + res2 + ")"
    return res1, res2


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        img_base64 = request.values["imageBase64"]
        print("predict" + img_base64)
        image_data = re.sub("^data:image/.+;base64,", "", img_base64)

        character, aksara = predict_fit(image_data)
        result = {"character": str(character), "aksara": str(aksara)}
        return jsonify(result)
    else:
        return "Predict"


if __name__ == "__main__":
    app.run()