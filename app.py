from flask import Flask, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

@app.get("/api/health")
def health():
    return jsonify(status="ok", time=datetime.now(timezone.utc).isoformat())

@app.get("/api/hello")
def hello():
    name = request.args.get("name", "world")
    return jsonify(message=f"Hello, {name}!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)