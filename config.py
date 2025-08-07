from flask import Flask, request, g
from prometheus_client import Counter
import os
from dotenv import load_dotenv
import time
from models import db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

REQUEST_COUNT = Counter(
    'flask_request_count',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'http_status']
)

@app.before_request
def _start_timer():
    g.start = time.time()

@app.after_request
def _record_and_print(response):
    labeled = REQUEST_COUNT.labels(request.method, request.path, response.status_code)
    labeled.inc()

    try:
        current = labeled._value.get()
    except AttributeError:
        current = "<unknown>"

    print(f"[metrics] {request.method} {request.path} {response.status_code} -> count={current}")

    return response

db.init_app(app)
with app.app_context():
    db.create_all()
