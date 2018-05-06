import os
import numpy as np
import cv2

from keras.models import Sequential, load_model, Model
from keras.layers import Input, Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Activation
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, CSVLogger
from keras.applications.vgg16 import VGG16
from keras.optimizers import SGD

epochs = 100
train_samples = 7500
validation_samples = 625

img_width, img_height = 150, 150

n_classes = 25
train_data_dir = './data/train'
valid_data_dir = './data/valid'

datagen = ImageDataGenerator(rescale=1./255)
batch_size = 32

train_generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size)

valid_generator = datagen.flow_from_directory(
    valid_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size)


def load_data():
    files = os.listdir('./good_images')
    base_names = [(os.path.basename(file).split('_0', 1)[0], os.path.join('./good_image', file)) for file in files]
    x_data = files
    y_data = [0]
    for i, base_name in enumerate(base_names[1:]):
        if base_name[0] == base_names[i][0]:
            y_data.append(y_data[-1])
        else:
            y_data.append(y_data[-1] + 1)
    y_data = to_categorical(y_data)
    return x_data, y_data


def train_model():
    model_vgg = VGG16(include_top=False, weights='imagenet', input_shape=(150, 150, 3))

    top_model = Sequential()
    top_model.add(Flatten(input_shape=model_vgg.output_shape[1:]))
    top_model.add(Dense(256))
    top_model.add(Activation('relu'))
    top_model.add(Dropout(0.5))

    top_model.add(Dense(256))

    features = top_model(model_vgg.output)

    extractor = Model(inputs=model_vgg.input, outputs=features)

    last = Activation('relu')(features)
    last = Dropout(0.5)(last)
    last = Dense(n_classes, activation='softmax')(last)

    model = Model(inputs=model_vgg.input, outputs=last)

    for layer in model.layers[:15]:
        layer.trainable = False

    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(lr=1e-4, momentum=0.9),
                  metrics=['accuracy'])

    checkpointer = ModelCheckpoint(filepath='./models/conv_model.h5', monitor='val_loss', verbose=1,
                                   save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_loss', verbose=1, patience=5)
    tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=batch_size, write_graph=True,
                              write_images=True)
    csv_logger = CSVLogger('training_vector.log')

    model.fit_generator(train_generator,
                        steps_per_epoch=train_samples // batch_size,
                        epochs=epochs,
                        validation_data=valid_generator,
                        validation_steps=validation_samples // batch_size,
                        callbacks=[checkpointer, tensorboard, early_stopping, csv_logger])
    return extractor


def main():
    if not os.path.exists('models'):
        os.mkdir('models')

    model = train_model()
    model.save('./models/model.h5')


if __name__ == '__main__':
    main()
