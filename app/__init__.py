import os
import sqlite3
from flask import Flask, render_template


def _init_db(db_path):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema = os.path.join(base, 'database', 'schema.sql')
    seed   = os.path.join(base, 'database', 'seed.sql')
    conn = sqlite3.connect(db_path)
    with open(schema, encoding='utf-8') as f:
        conn.executescript(f.read())
    with open(seed, encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def create_app():
    app = Flask(__name__)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path  = os.path.join(base_dir, 'database', 'pickpet.db')
    app.config['DB_PATH'] = db_path
    app.secret_key = 'pickpet-dev-secret-2025'

    if not os.path.exists(db_path):
        _init_db(db_path)

    # Provide stub globals for templates that reference auth (not yet implemented)
    class _AnonUser:
        is_authenticated = False
        role = None
    app.jinja_env.globals['current_user'] = _AnonUser()
    app.jinja_env.globals['csrf_token']   = lambda: ''

    @app.route('/')
    def index():
        return render_template('index.html')

    from app.dogs.routes import dogs_bp
    app.register_blueprint(dogs_bp)

    return app
