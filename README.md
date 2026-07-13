first-api

The smallest possible backend: a Flask server with two JSON endpoints.


GET /api/health → {"status": "ok", "time": "<UTC timestamp>"}
GET /api/hello?name=Ada → {"message": "Hello, Ada!"} (name is optional, defaults to "world")


1. Run it locally

bashpython3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py

The server starts on http://127.0.0.1:5000.

2. Call it

From curl:

bashcurl http://127.0.0.1:5000/api/health
curl "http://127.0.0.1:5000/api/hello?name=Ada"

From your browser: just open
http://127.0.0.1:5000/api/health and
http://127.0.0.1:5000/api/hello?name=Ada
