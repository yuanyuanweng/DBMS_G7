from flask import Flask, session
from app.database import close_db, get_db
import sqlite3

def _add_seen_column(app):
    """Add Seen column to Application if it doesn't exist yet."""
    try:
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.execute(
            "ALTER TABLE Application ADD COLUMN Seen INTEGER NOT NULL DEFAULT 1"
        )
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        pass  # column already exists


def _add_favorite_table(app):
    """Create Favorite table if it doesn't exist yet."""
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Favorite (
            User_ID INTEGER NOT NULL,
            Dog_ID INTEGER NOT NULL,
            Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (User_ID, Dog_ID),
            FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
            FOREIGN KEY (Dog_ID) REFERENCES Dog(Dog_ID)
        )
    """)
    conn.commit()
    conn.close()


def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = "database/pickpet.db"
    app.config["SECRET_KEY"] = "pickpet-secret-key-2025"
    app.teardown_appcontext(close_db)
    
    _add_seen_column(app)
    _add_favorite_table(app)

    from app.main_routes import main
    from app.dogs.routes import dogs_bp
    from app.auth.routes import auth_bp
    from app.applications.routes import applications_bp
    from app.admin.routes import admin_bp
    from app.ai.routes import ai_bp

    app.register_blueprint(main)
    app.register_blueprint(dogs_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(ai_bp)

    @app.context_processor
    def inject_notif_count():
        user_id = session.get('user_id')
        if not user_id:
            return {'notif_count': 0}
        try:
            db = get_db()
            count = db.execute(
                'SELECT COUNT(*) FROM Application WHERE User_ID = ? AND Seen = 0 AND Status != 0',
                (user_id,)
            ).fetchone()[0]
        except Exception:
            count = 0
        return {'notif_count': count}

    return app
