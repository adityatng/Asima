from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_minify import minify
import tensorflow as tf
from keras.models import load_model
from keras.utils import img_to_array
import re
import pandas as pd
import numpy as np
import base64
import io
from PIL import Image

app = Flask(__name__)
minify(app=app, html=True, js=True, cssless=True)

# Parameters
input_size = (30, 30)
# define input shape
channel = (3,)
input_shape = input_size + channel
# define labels
labels = [
    "A",
    "Ba",
    "Da",
    "Ga",
    "Ha",
    "I",
    "Ja",
    "Ka",
    "La",
    "Ma",
    "Na",
    "Nga",
    "Nya",
    "Pa",
    "Ra",
    "Sa",
    "Ta",
    "U",
    "Wa",
    "Ya",
]


def preprocess(img, input_size):
    nimg = img.convert("RGB").resize(input_size, resample=0)
    img_arr = (np.array(nimg)) / 255
    return img_arr


def reshape(imgs_arr):
    return np.stack(imgs_arr, axis=0)


def predict_fit(image_data):
    MODEL_PATH = "model/asima_Model.h5"
    model = load_model(MODEL_PATH, compile=False)
    img = base64.b64decode(image_data)
    im = Image.open(io.BytesIO(img))

    #adding bgcolor
    fill_color = (225,225,225)  # your new background color
    im = im.convert("RGBA")   # it had mode P after DL it from OP
    if im.mode in ('RGBA', 'LA'):
        background = Image.new(im.mode[:-1], im.size, fill_color)
        background.paste(im, im.split()[-1]) # omit transparency
        im = background
    im.convert("RGB")

    X = preprocess(im, input_size)
    X = reshape([X])
    y = model.predict(X)

    res1 = labels[np.argmax(y)]
    res2 = (100 * np.max(y)).round(2)
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

        digit, accuracy = predict_fit(image_data)
        results = {"character": str(digit), "accuracy": float(accuracy)}
        return jsonify(results)
    else:
        return "Predict"


if __name__ == "__main__":
    app.run()
