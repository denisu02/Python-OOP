from flask import jsonify
from datetime import datetime
from models import RequestLog, db

def log(op, inp, res):
    entry = RequestLog(operation=op, input_data=str(inp), result=str(res),
                       timestamp=datetime.utcnow())
    db.session.add(entry)
    db.session.commit()


def get_logs():
    logs = RequestLog.query.order_by(RequestLog.timestamp.desc()).all()
    return jsonify([
        {'operation': log.operation, 'input': log.input_data,
         'result': log.result, 'time': log.timestamp.isoformat()}
        for log in logs
    ])
