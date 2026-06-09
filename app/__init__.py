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


def _add_dog_description_column(app):
    """Add Description column to Dog if it doesn't exist yet."""
    try:
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.execute("ALTER TABLE Dog ADD COLUMN Description TEXT")
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


def _refresh_dog_status_view(app):
    """Recreate Dog_With_Status so it matches the current Dog columns."""
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.execute("DROP VIEW IF EXISTS Dog_With_Status")
    conn.execute("""
        CREATE VIEW Dog_With_Status AS
        SELECT
            d.Dog_ID,
            d.Shelter_ID,
            d.Name,
            d.Gender,
            d.Age,
            d.Breed,
            d.Image_URL,
            d.Description,
            CASE
                WHEN COUNT(CASE WHEN a.Status = 1 THEN 1 END) > 0 THEN 'Adopted'
                WHEN COUNT(CASE WHEN a.Status = 0 THEN 1 END) > 0 THEN 'Pending'
                ELSE 'Available'
            END AS Availability
        FROM Dog d
        LEFT JOIN Application a
            ON d.Dog_ID = a.Dog_ID
        GROUP BY d.Dog_ID
    """)
    conn.commit()
    conn.close()


def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = "database/pickpet.db"
    app.config["SECRET_KEY"] = "pickpet-secret-key-2025"
    app.teardown_appcontext(close_db)
    
    _add_seen_column(app)
    _add_dog_description_column(app)
    _add_favorite_table(app)
    _refresh_dog_status_view(app)

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
