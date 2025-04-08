from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return "ML Model is Running"

# Exercise 4
@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    # Exercise 3
    if "features" not in data:
        return jsonify({"error": "'features' key is missing"}), 400
    
    features = data["features"]

    for feature in features:
        if len(feature) != 4:
            return jsonify({"error": "Each input must have exactly 4 features"}), 400
        if not all(isinstance(x, (float, int)) for x in feature):
            return jsonify({"error": "Each feature value must be a float"}), 400
        
    input_features = np.array(data["features"])
    prediction = model.predict(input_features)
    # Exercise 2
    confident_score = model.predict_proba(input_features)
    confidence = [confident_score[i][prediction[i]] for i in range(len(prediction))]

    return jsonify({
        "predictions": prediction.tolist(),
        # Exercise 1
        "confidences": confidence
    })

# Exercise 5

with open("linear_model.pkl", "rb") as f:
    linear_model = pickle.load(f)

@app.route("/predict_price", methods=["POST"])
def predict_price():
    data = request.get_json()
    try:
        features = data["features"]
        predictions = linear_model.predict(features)
        return jsonify({"predictions": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000) #check your port number ( if it is in use, change the port number)