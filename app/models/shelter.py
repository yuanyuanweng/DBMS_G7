from app.database import get_db

class Shelter:
    def __init__(self, row):
        """Create a Shelter object from one database row."""
        self.id = row["Shelter_ID"]
        self.name = row["Name"]
        self.location = row["Location"]
        self.contact = row["Contact"]

    def to_dict(self):
        """Convert the shelter object into a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "contact": self.contact,
        }

    @staticmethod
    def get_all():
        """Return all shelters ordered by name."""
        db = get_db()
        rows = db.execute(
            """
            SELECT Shelter_ID, Name, Location, Contact
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
            SELECT Shelter_ID, Name, Location, Contact
            FROM Shelter
            WHERE Shelter_ID = ?
            """,
            (shelter_id,),
        ).fetchone()
        return Shelter(row) if row else None

    @staticmethod
    def get_by_user_id(user_id):
        """Return shelters assigned to one staff/admin user."""
        db = get_db()
        rows = db.execute(
            """
            SELECT s.Shelter_ID, s.Name, s.Location, s.Contact
            FROM Shelter s
            JOIN User_Shelter us ON s.Shelter_ID = us.Shelter_ID
            WHERE us.User_ID = ?
            ORDER BY s.Name
            """,
            (user_id,),
        ).fetchall()
        return [Shelter(row) for row in rows]
