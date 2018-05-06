from keras.preprocessing import image
import numpy as np
import os


def extract_embedding(embedding_model, img_file):
    img = image.load_img(img_file, target_size=(150, 150))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    embeddings = embedding_model.predict(img_tensor)
    return embeddings


def predict(embedding_model, svm_model, img_file):
    embeddings = extract_embedding(embedding_model, img_file)
    pred = svm_model.predict(embeddings)
    return int(pred)
