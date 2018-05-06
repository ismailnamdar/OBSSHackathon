from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
from keras.utils import to_categorical
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score


def train_svm():
    # model_file = './models/conv_model.h5'
    # places = os.listdir('./data/train')
    # model = load_model(model_file)
    # x_train = []
    # y_train = []
    # for i, place in enumerate(places):
    #     files = os.listdir(os.path.join('./data/train', place))
    #     files = [file for file in files if file.endswith('.npy')]
    #     for file in files:
    #         vector = model.predict(np.load(os.path.join('./data/train', place, file)))
    #         x_train.append(vector.T)
    #         y_train.append(i)
    # x_train = np.squeeze(np.array(x_train))
    # y_train = np.array(y_train)
    # np.save('x_train_svm.npy', x_train)
    # np.save('y_train_svm.npy', y_train)
    x_train = np.load('x_train_svm.npy')
    y_train = np.load('y_train_svm.npy')

    clf = svm.SVC()
    clf.fit(x_train, y_train)
    joblib.dump(clf, './models/svm_model.pkl')


def test_svm():
    model_file = './models/conv_model.h5'
    places = os.listdir('./data/train')
    model = load_model(model_file)
    x_test = []
    y_test = []
    for i, place in enumerate(places):
        files = os.listdir(os.path.join('./data/valid', place))
        files = [file for file in files if file.endswith('.npy')]
        for file in files:
            vector = model.predict(np.load(os.path.join('./data/valid', place, file)))
            x_test.append(vector.T)
            y_test.append(i)
    x_test = np.squeeze(np.array(x_test))
    y_test = np.array(y_test)
    np.save('x_test_svm.npy', x_test)
    np.save('y_test_svm.npy', y_test)

    clf = joblib.load('./models/svm_model.pkl')
    y_pred = clf.predict(x_test)
    score = accuracy_score(y_test, y_pred)
    print(score)


if __name__ == '__main__':
    train_svm()
    test_svm()
