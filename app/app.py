from pathlib import Path
import sqlite3
import sys
from flask import Flask, jsonify, render_template

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT.parent / 'logs'
DATA_DIR = ROOT.parent / 'data'
LOG_FILE = LOG_DIR / 'application.log'
DATA_FILE = DATA_DIR / 'notes.db'

try:
    from app.config import APP_NAME, PORT, SERVICE_USER
except ImportError as error:
    raise ImportError('Failed to load configuration file: app/config.py') from error

app = Flask(__name__, template_folder=str(ROOT / 'templates'))


def configure_logger():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open('a') as handle:
        handle.write('')


def get_notes():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        return []
    with sqlite3.connect(DATA_FILE) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT id, title, body FROM notes ORDER BY id')
        return [dict(row) for row in cursor.fetchall()]


@app.route('/')
def home():
    return render_template('index.html', app_name=APP_NAME)


@app.route('/health')
def health():
    return jsonify(status='healthy')


@app.route('/notes')
def notes():
    return jsonify(notes=get_notes())


if __name__ == '__main__':
    try:
        configure_logger()
    except PermissionError as error:
        raise PermissionError(f'Unable to open log file {LOG_FILE}: {error}')

    print(f'Starting {APP_NAME} on port {PORT} as {SERVICE_USER}')
    app.run(host='0.0.0.0', port=PORT)
