from pymongo import MongoClient
from backend.GazeDetector import GazeDetector

detector = GazeDetector()
client = MongoClient('mongodb://JohnH:johnhoward@ds231228.mlab.com:31228/eyedata-devel')
db = client['eyedata-devel']
collection = db.Frames

cursor = collection.find({})
all_data = [k for k in cursor]
data = [item['x'][1:] for item in all_data]
labels = [item['y'] for item in all_data]

detector.train_location_classifier(data, labels, 500)
detector.test_accuracy(data, labels)


model_json = detector.neural_network.to_json()
with open("backend/model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
detector.neural_network.save_weights("backend/model_weights.h5")
