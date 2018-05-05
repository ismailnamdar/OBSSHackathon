from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os


def predict(model_file, img_file):
    model = load_model(model_file)
    img = image.load_img(img_file, target_size=(150, 150))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    pred = model.predict(img_tensor)
    return np.argmax(pred)
