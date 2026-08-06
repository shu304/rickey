from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data_store = []

@app.route("/api/answers", methods=["GET"])
def get_answers():
    return jsonify(data_store)

@app.route("/api/answers", methods=["POST"])
def post_answer():
    data = request.json
    data_store.append(data)
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(port=5000)