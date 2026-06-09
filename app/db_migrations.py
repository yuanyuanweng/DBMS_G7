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


def run_startup_migrations(app):
    """Keep older local SQLite databases compatible with the current app."""
    _add_seen_column(app)
    _add_dog_description_column(app)
    _add_favorite_table(app)
    _refresh_dog_status_view(app)
