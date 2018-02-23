import atexit
import os
import subprocess as sp
import numpy as np
from time import sleep
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical

from backend.ipc_reader import IPCReader


class GazeDetector:
    LEFT_EYE = 0
    RIGHT_EYE = 1

    def __init__(self, external_camera=False):

        # TODO: parameterize so that we can pass in the camera number
        self.cpp_proc = sp.Popen(['{prefix}/backend/eyefinder_cpp/build/eyefinder'.format(prefix=os.getcwd())])

        # clean up IPC at end
        atexit.register(self.cleanup)
        sleep(2)
        self.active = (self.cpp_proc.poll() is not None)

        self.neural_network = None
        self.init_model()

        self.last_id_seen = -1

    def init_model(self):
        model = Sequential()
        model.add(Dense(20, input_shape=(4,), kernel_initializer='uniform', activation='relu'))
        model.add(Dense(20, kernel_initializer='uniform', activation='relu'))
        # model.add(Dense(20, kernel_initializer='uniform', activation='sigmoid'))
        model.add(Dense(4, activation="softmax"))
        model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.02))
        self.neural_network = model

    def sample(self):
        """
        Read an image from the video capture device and determine where the user is looking
        :return: a ndarray of probabilities for each label in the UI
        """

        # TODO: check if seen frame already

        features = self.sample_features()

        # print(features)
        feature_id = features[0]

        while feature_id == self.last_id_seen:
            features = self.sample_features()

        self.last_id_seen = feature_id

        probabilities = self.calculate_location_probabilities_from_features(features[25:29])

        return probabilities

    def cleanup(self):
        """
        Clean up the semaphore, shared memory, and kill the eye finder process
        """
        with IPCReader() as reader:
            reader.clean()
        self.cpp_proc.kill()

    @staticmethod
    def sample_features():
        """
        Read an image from the video capture device and return the extracted features of the image
        :return: a ndarray of shape(30) full of numerical features
        """
        with IPCReader() as reader:
            return np.asarray(reader.read())

    def calculate_location_probabilities_from_features(self, features):
        """
        Feed features through a machine learning algorithm to get probabilities
        :param features: a ndarray of shape(30) full of numerical features
        :return: a ndarray of probabilities for each label in the UI
        """

        features = np.asarray([features, ])

        prediction_vals = self.neural_network.predict(features)
        return prediction_vals

    def train_location_classifier(self, data, labels, num_epochs=1000):
        """
        Train location classifier using data
        :param data: a ndarray of shape(N, 30) of N rows of numerical features
        :param num_epochs: an integer number for how many iterations through all the data the training will do
        """

        np_data = np.asarray(data)
        categorical_labels = to_categorical(labels)

        self.neural_network.fit(np_data, categorical_labels, epochs=num_epochs)


if __name__ == '__main__':
    tracker = GazeDetector()
    sleep(1)
    for i in range(100):
        sleep(0.05)
        tracker.sample()
