from pymongo import MongoClient
from backend.GazeDetector import GazeDetector


detector = GazeDetector(use_cpp=False, load_model=False)
client = MongoClient('mongodb://JohnH:johnhoward@ds231228.mlab.com:31228/eyedata-devel')
db = client['eyedata-devel']
collection = db.Test

cursor = collection.find({})
all_data = [k for k in cursor]
data = [detector.extract_used_features(item['x']) for item in all_data]
labels = [item['y'] for item in all_data]

detector.train_location_classifier(data, labels, 600)
detector.test_accuracy(data, labels)

# write out to file
model_json = detector.neural_network.to_json()
with open("backend/model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
detector.neural_network.save_weights("backend/model_weights.h5")
