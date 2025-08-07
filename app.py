import asyncio
from flask import request, jsonify
from config import app
from math_utils import fact, fibo
from logging_utils import log, get_logs


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
def logs_route():
    return get_logs()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
