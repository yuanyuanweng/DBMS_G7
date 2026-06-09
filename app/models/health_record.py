from app.database import get_db


class HealthRecord:
    @staticmethod
    def create(dog_id, administered_date, vaccine_name):
        """Create a health record and return the new record ID."""
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO Health_record (Dog_ID, Administered_Date, Vaccine_Name)
            VALUES (?, ?, ?)
            """,
            (dog_id, administered_date, vaccine_name),
        )
        db.commit()
        return cursor.lastrowid
