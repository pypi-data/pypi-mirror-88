import sys
import time
import json
import sqlite3
import argparse

from pathlib import Path

from flask import Flask, g
from flask import render_template

app = Flask(__name__)

CURRENT_PATH = Path(__file__)
DB_FILE_PATH = CURRENT_PATH.parent / 'prices.db'

@app.before_request
def before_request():
    g.db = sqlite3.connect(str(DB_FILE_PATH))


@app.teardown_request
def teardown_request_func(error=None):
    g.db.close()


def get_exchanges(db):
    cursor = db.execute("SELECT DISTINCT exchange FROM price ORDER BY exchange ASC;")
    results = cursor.fetchall()
    return [exc for sub in results for exc in sub]

def get_symbols(db):
    cursor = db.execute("SELECT DISTINCT symbol FROM price ORDER BY symbol ASC;")
    results = cursor.fetchall()
    return [exc for sub in results for exc in sub]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/exchanges')
def exchanges():
    exchanges = get_exchanges(g.db)
    return json.dumps(exchanges), 200, {'Content-Type': 'application/json'}


@app.route('/symbols')
def symbols():
    symbols = get_symbols(g.db)
    return json.dumps(symbols), 200, {'Content-Type': 'application/json'}


@app.route('/price/<exchange>/<symbol>/<date>')
def price(exchange, symbol, date):
    g.db.row_factory = sqlite3.Row
    cursor = g.db.execute("""
        SELECT exchange, symbol, open, high, low, close, volume, day FROM price
        WHERE exchange = ? AND symbol = ? AND day = ?;
    """, (exchange, symbol, date))
    results = [dict(r) for r in cursor.fetchall()]
    result = None
    if len(results):
        result = results[0]
    if app.config['SLEEP']:
        time.sleep(app.config['SLEEP'])
    return json.dumps(result), 200, {'Content-Type': 'application/json'}


def main():
    parser = argparse.ArgumentParser(description='Runs the tiny crypto server')
    parser.add_argument('--sleep', help='time to sleep (in seconds) before each request', type=int, required=False, default=None)
    parser.add_argument('--host', help='Server host', required=False, default="0.0.0.0")
    parser.add_argument('--port', help='Server port', type=int, required=False, default=8080)
    args = parser.parse_args()

    app.debug = True
    app.config['SLEEP'] = args.sleep
    app.run(port=args.port, host=args.host)


if __name__ == '__main__':
    main()
