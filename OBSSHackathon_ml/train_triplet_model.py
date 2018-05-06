import os
import numpy as np
import random

from keras.models import Sequential, load_model, Model
from keras.layers import Input, Dense, Dropout, Flatten, Lambda
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Activation
from keras.layers.merge import add, concatenate, dot
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, CSVLogger
from keras.applications.xception import Xception
from keras.optimizers import SGD
from keras import backend as K

epochs = 100
train_samples = 7500
validation_samples = 625

img_width, img_height = 150, 150

n_classes = 25
train_data_dir = './triplet_data/train'
valid_data_dir = './triplet_data/valid'

batch_size = 32


def hinge_abs(y_true, y_pred):
    return K.mean(K.abs(0.6 - y_true * y_pred), axis=-1)


def create_triplets(set):
    size = 2500 if set == 'train' else 625
    x_data = np.empty((3, size, 150, 150, 3))
    y_data = np.empty((size, 1))
    places = os.listdir('./triplet_data/' + set)
    all_files = []
    for i, place in enumerate(places):
        files = os.listdir(os.path.join('./triplet_data', set, place))
        all_files.extend([(i, os.path.join('./triplet_data', set, place, file)) for file in files if file.endswith('.npy')])

    for i, file in enumerate(all_files):
        if i < len(all_files) - 1 and all_files[i+1][0] == file[0]:
            diff = random.choice(all_files)
            while diff[0] == file[0]:
                diff = random.choice(all_files)
            x_data[0][i] = np.load(file[1])
            x_data[1][i] = np.load(all_files[i+1][1])
            x_data[2][i] = np.load(diff[1])
            y_data[i] = 0.6

    return x_data, y_data


def train_model():
    model_xcept = Xception(include_top=False, weights='imagenet', input_shape=(150, 150, 3))

    top_model = Sequential()
    top_model.add(Flatten(input_shape=model_xcept.output_shape[1:]))
    top_model.add(Dense(256))
    top_model.add(Activation('relu'))
    top_model.add(Dropout(0.5))

    top_model.add(Dense(256))

    features = top_model(model_xcept.output)

    extractor = Model(inputs=model_xcept.input, outputs=features)

    last = Activation('relu')(features)
    last = Dropout(0.5)(last)

    final = Model(inputs=model_xcept.input, outputs=last)

    # x_train, y_train = create_triplets('train')
    # np.save('x_train', x_train)
    # np.save('y_train', y_train)
    # x_valid, y_valid = create_triplets('valid')
    # np.save('x_valid', x_valid)
    # np.save('y_valid', y_valid)
    x_train, y_train = np.load('x_train.npy'), np.load('y_train.npy')
    x_valid, y_valid = np.load('x_valid.npy'), np.load('y_valid.npy')

    input_a = Input(shape=(150, 150, 3))
    input_s = Input(shape=(150, 150, 3))
    input_d = Input(shape=(150, 150, 3))

    xa = final(input_a)
    xs = final(input_s)
    xd = final(input_d)
    a_s = dot([xa, xs], axes=-1)
    a_d = dot([xa, xd], axes=-1)
    w_final = Dense(1, input_shape=(1,), activation='sigmoid', use_bias=False,
                    trainable=False, weights=np.ones((1, 1))[:, np.newaxis])

    as_final = w_final(a_s)
    ad_final = w_final(a_d)
    subtract_layer = Lambda(lambda inputs: inputs[0] - inputs[1],
                            output_shape=lambda shapes: shapes[0])

    asd_hinge = subtract_layer([as_final, ad_final])

    model = Model(inputs=[input_a, input_s, input_d], output=[asd_hinge])

    for layer in model.layers[:15]:
        layer.trainable = False

    model.compile(loss=hinge_abs,
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    checkpointer = ModelCheckpoint(filepath='./models/model.h5', monitor='val_loss', verbose=1,
                                   save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_loss', verbose=1, patience=5)
    tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=batch_size, write_graph=True,
                              write_images=True)
    csv_logger = CSVLogger('training_vector.log')

    model.fit([x_train[0], x_train[1], x_train[2]], y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=([x_valid[0], x_valid[1], x_valid[2]], y_valid),
              callbacks=[checkpointer, tensorboard, early_stopping, csv_logger])
    return extractor


def main():
    if not os.path.exists('models'):
        os.mkdir('models')

    model = train_model()
    model.save('./models/model.h5')


if __name__ == '__main__':
    main()
