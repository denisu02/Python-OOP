from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class RequestLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(32), nullable=False)
    input_data = db.Column(db.String(64), nullable=False)
    result = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime)
