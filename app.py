from flask import Flask, render_template, request
import pickle
import socket
import re

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

def extract_features(url):
    features = []

    # 1. URL length
    features.append(len(url))

    # 2. HTTPS check
    features.append(1 if "https" in url else 0)

    # 3. @ symbol
    features.append(1 if "@" in url else 0)

    # 4. IP address check
    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"
    features.append(1 if re.search(ip_pattern, url) else 0)

    return features

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None

    if request.method == "POST":
        url = request.form["url"]
        features = [extract_features(url)]
        result = model.predict(features)

        if result[0] == 1:
            prediction = "Phishing ❌"
        else:
            prediction = "Legitimate ✅"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
