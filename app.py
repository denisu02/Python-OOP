import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from models import db, RequestLog
from datetime import datetime


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
with app.app_context():
    db.create_all()


def fact(x):
    res = 1
    for i in range(2, x + 1):
        res = res * i
    return res


def fibo(x):
    a = 0
    b = 1
    for i in range(x):
        a = b
        b = a + b
    return a


@app.route('/')
def index():
    return '''
    <html>
    <link rel="stylesheet" href="/static/style.css">
      <head><title>OOP Python</title></head>
      <body>
        <h1>OOP Python</h1>
        <form action="/pow" method="get">
          <h3>Power</h3>
          a: <input name="a" type="text" /> <br>
          b: <input name="b" type="text" /> <br><br>
          <button type="submit">Power(a^b)</button>
        </form>
        <form action="/fib/" method="get"
        onsubmit="this.action='/fib/'+this.n.value;">
          <h3>Fibonacci</h3>
          n: <input name="n" type="number" min="0" /> <br><br>
          <button type="submit">Fibonacci(n)</button>
        </form>
        <form action="/factorial/" method="get"
        onsubmit="this.action='/factorial/'+this.n.value;">
          <h3>Factorial</h3>
          n: <input name="n" type="number" min="0" /> <br><br>
          <button type="submit">Factorial n!</button>
          <br>
        </form>
        <h3>Logs</h3>
        <a href="/logs">Logs</a>
      </body>
    </html>
    '''


def log(op, inp, res):
    entry = RequestLog(operation=op, input_data=str(inp), result=str(res),
                       timestamp=datetime.utcnow())
    db.session.add(entry)
    db.session.commit()


@app.route('/pow')
async def power():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
        result = await asyncio.to_thread(lambda: a ** b)
        log('pow', {'a': a, 'b': b}, result)
        return jsonify(operation='power',
                       input={'a': a, 'b': b}, result=result)
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route('/fib/<int:n>')
async def fibonacci(n):
    if n < 0:
        return jsonify(error='n must be > 0'), 400

    result = await asyncio.to_thread(fibo, n)
    log('fibonacci', {'n': n}, result)
    return jsonify(operation='fibonacci', input={'n': n}, result=result)


@app.route('/factorial/<int:n>')
async def factorial(n):
    if n < 0:
        return jsonify(error='n must be > 0'), 400

    result = await asyncio.to_thread(fact, n)
    log('factorial', {'n': n}, result)
    return jsonify(operation='factorial', input={'n': n}, result=result)


@app.route('/logs')
def get_logs():
    logs = RequestLog.query.order_by(RequestLog.timestamp.desc()).all()
    return jsonify([
        {'operation': log.operation, 'input': log.input_data,
         'result': log.result, 'time': log.timestamp.isoformat()}
        for log in logs
    ])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
