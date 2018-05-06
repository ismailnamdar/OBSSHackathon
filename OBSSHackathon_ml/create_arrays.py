import os
import numpy as np
from keras.preprocessing.image import load_img, img_to_array

places = os.listdir('./data/valid')
for place in places:
    files = os.listdir(os.path.join('./data/valid', place))
    for file in files:
        file_name = os.path.join('./data/valid', place, file)
        img = load_img(file_name, target_size=(150, 150))
        img_tensor = img_to_array(img)
        img_tensor = np.expand_dims(img_tensor, axis=0)
        img_tensor /= 255.
        np.save('.' + file_name.split('.')[1], img_tensor)