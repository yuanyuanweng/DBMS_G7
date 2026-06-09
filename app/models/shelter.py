from app.database import get_db

class Shelter:
    def __init__(self, row):
        """Create a Shelter object from one database row."""
        self.id = row["Shelter_ID"]
        self.name = row["Name"]
        self.location = row["Location"]

    @staticmethod
    def get_all():
        """Return all shelters ordered by name."""
        db = get_db()
        rows = db.execute(
            """
            SELECT Shelter_ID, Name, Location
            FROM Shelter
            ORDER BY Name
            """
        ).fetchall()
        return [Shelter(row) for row in rows]

    @staticmethod
    def get_by_id(shelter_id):
        """Return one shelter by its shelter ID."""
        db = get_db()
        row = db.execute(
            """
            SELECT Shelter_ID, Name, Location
            FROM Shelter
            WHERE Shelter_ID = ?
            """,
            (shelter_id,),
        ).fetchone()
        return Shelter(row) if row else None
