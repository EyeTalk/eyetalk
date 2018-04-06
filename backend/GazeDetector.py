import atexit
import os
import sys
import subprocess as sp
import numpy as np
from time import sleep
from keras.layers import Dense
from keras.models import Sequential, model_from_json
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from keras.callbacks import Callback, ReduceLROnPlateau, EarlyStopping

from collections import deque

from backend.ipc_reader import IPCReader


class GazeDetector:
    DEFAULT_BLINK_THRESHOLD = 0.35

    def __init__(self, load_model=False, use_cpp=True):
        """
        The use_cpp parameter is used to make it easy to do machine learning training without running the backend too.
        """

        self.cpp_proc = None
        self.active = False

        if use_cpp:
            self.init_cpp_backend()

        # clean up IPC at end
        atexit.register(self.cleanup)

        self.neural_network = None

        if load_model:
            self.load_model_from_file()
        else:
            self.init_model()

        self.last_id_seen = -1
        self.last_probabilities = None
        self.last_blink = False

        self.training_epochs = 0
        self.current_epoch = 0
        self.current_accuracy = 0.0
        self.blink_threshold = self.DEFAULT_BLINK_THRESHOLD

        self.blink_deque = deque(maxlen=3)

    def init_cpp_backend(self):
        for _ in range(3):
            self.cpp_proc = sp.Popen(['{prefix}/backend/eyefinder_cpp/build/eyefinder'.format(prefix=os.getcwd())])
            sleep(2)
            self.active = (self.cpp_proc.poll() is None)

            if self.active:
                return
            else:
                self.cpp_proc.terminate()
                self.cpp_proc = None
                self.cleanup()
                sleep(2)
        sys.exit('The program is unable to start the eye tracking system')

    def init_model(self):
        model = Sequential()
        model.add(Dense(20, input_shape=(9,), kernel_initializer='uniform', activation='relu'))
        model.add(Dense(20, kernel_initializer='uniform', activation='relu'))
        model.add(Dense(11, activation="softmax"))
        model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.025), metrics=['accuracy'])
        self.neural_network = model

    def load_model_from_file(self):
        with open('backend/model.json', 'r') as f:
            loaded_model_json = f.read()
            f.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("backend/model_weights.h5")
        loaded_model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.025), metrics=['accuracy'])

        self.neural_network = loaded_model

    def sample(self):
        """
        Read an image from the video capture device and determine where the user is looking
        :return: a ndarray of probabilities for each label in the UI
        """

        features = self.sample_features()

        feature_id = features[0]

        if feature_id != self.last_id_seen:

            self.last_id_seen = feature_id

            used_features = self.extract_used_features(features)
            blinking = self.detect_blink(features)
            self.last_blink = blinking
            probabilities = self.calculate_location_probabilities_from_features(used_features)
            self.last_probabilities = probabilities

        else:
            blinking = self.last_blink
            probabilities = self.last_probabilities

        return feature_id, blinking, probabilities

    def detect_blink(self, features):
        left_eye_aspect_ratio = features[1]
        right_eye_aspect_ratio = features[2]

        average_ratio = (left_eye_aspect_ratio + right_eye_aspect_ratio) / 2

        self.blink_deque.appendleft(average_ratio)
        all_samples = tuple(self.blink_deque)
        smoothed_average = sum(all_samples) / len(all_samples)

        return smoothed_average < self.blink_threshold

    @staticmethod
    def calculate_eye_ratio(eye_features):
        eye_points = [np.asarray([eye_features[2 * i], eye_features[2 * i + 1]]) for i in range(6)]

        ratio_top = np.linalg.norm(eye_points[1] - eye_points[5]) + np.linalg.norm(eye_points[2] - eye_points[4])
        ratio_bottom = np.linalg.norm(eye_points[0] - eye_points[3]) * 2.0

        return ratio_top / ratio_bottom

    def set_new_blink_threshold(self, baseline_eye_ratio):
        self.blink_threshold = baseline_eye_ratio * 0.85

    def cleanup(self):
        """
        Clean up the semaphore, shared memory, and kill the eye finder process
        """
        try:
            with IPCReader() as reader:
                reader.clean()
            self.cpp_proc.kill()
        except Exception:
            pass

    @staticmethod
    def sample_features():
        """
        Read an image from the video capture device and return the extracted features of the image
        :return: a ndarray of shape(30) full of numerical features
        """
        with IPCReader() as reader:
            return np.asarray(reader.read())

    def extract_used_features(self, vector):
        return vector[1:-2]

    def calculate_location_probabilities_from_features(self, features):
        """
        Feed features through a machine learning algorithm to get probabilities
        :param features: a ndarray of shape(30) full of numerical features
        :return: a ndarray of probabilities for each label in the UI
        """

        features = np.asarray([features, ])

        prediction_vals = self.neural_network.predict(features)
        return prediction_vals

    def train_location_classifier(self, data, labels, num_epochs=750, patience=100):
        """
        Train location classifier using data
        :param data: a ndarray of shape(N, 11) of N rows of numerical features
        :param num_epochs: an integer number for how many iterations through all the data the training will do
        """

        np_data = np.asarray(data)
        categorical_labels = to_categorical(labels)

        self.training_epochs = num_epochs

        progress_callback = ProgressCallback(self)
        lr_callback = ReduceLROnPlateau(patience=25, monitor='acc')
        stop_callback = EarlyStopping(patience=patience, monitor='acc')
        callbacks = [progress_callback, lr_callback, stop_callback]

        self.neural_network.fit(np_data, categorical_labels, epochs=num_epochs, callbacks=callbacks)

    def test_accuracy(self, data, labels):
        """
        Print out the accuracy of the predictions on a given set of data and labels
        :param data: a list of np arrays
        :param labels: a list of integers labels in the range [0, 10]
        """

        total = 0
        count = 0

        for i in range(len(data)):
            test_data = data[i]
            test_label = labels[i]
            probabilities = self.calculate_location_probabilities_from_features(test_data)
            predicted_label = np.argmax(probabilities)
            count += int(predicted_label == test_label)
            total += 1

        percent = count * 1.0 / total

        print('Percent correct:', percent)
        return percent


class ProgressCallback(Callback):
    def __init__(self, detector):
        Callback.__init__(self)
        self.detector = detector

    def on_epoch_end(self, epoch, logs=None):
        self.detector.current_epoch = epoch
        self.detector.current_accuracy = logs['acc']
