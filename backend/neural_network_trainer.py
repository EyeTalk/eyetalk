from pymongo import MongoClient
from backend.GazeDetector import GazeDetector
from keras.models import model_from_json

detector = GazeDetector()
client = MongoClient('mongodb://JohnH:johnhoward@ds231228.mlab.com:31228/eyedata-devel')
db = client['eyedata-devel']
collection = db.Frames

cursor = collection.find({})
all_data = [k for k in cursor]
data = [item['x'][1:] for item in all_data]
labels = [item['y'] for item in all_data]

detector.train_location_classifier(data, labels, 1000)


model_json = detector.neural_network.to_json()
with open("backend/test_model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
detector.neural_network.save_weights("backend/test_model.h5")

# # load json and create model
# json_file = open('test_model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# # load weights into new model
# loaded_model.load_weights("test_model.h5")
# print("Loaded model from disk")