from app.database import get_db

class HealthRecord:
    def __init__(self, row):
        """Create a HealthRecord object from one database row."""
        self.id = row["Record_ID"]
        self.dog_id = row["Dog_ID"]
        self.administered_date = row["Administered_Date"]
        self.vaccine_name = row["Vaccine_Name"]

    def to_dict(self):
        """Convert the health record object into a dictionary."""
        return {
            "id": self.id,
            "dog_id": self.dog_id,
            "administered_date": self.administered_date,
            "vaccine_name": self.vaccine_name,
        }

    @staticmethod
    def get_by_id(record_id):
        """Return one health record by its record ID."""
        db = get_db()
        row = db.execute(
            """
            SELECT Record_ID, Dog_ID, Administered_Date, Vaccine_Name
            FROM Health_record
            WHERE Record_ID = ?
            """,
            (record_id,),
        ).fetchone()
        return HealthRecord(row) if row else None

    @staticmethod
    def get_by_dog_id(dog_id):
        """Return all health records for one dog."""
        db = get_db()
        rows = db.execute(
            """
            SELECT Record_ID, Dog_ID, Administered_Date, Vaccine_Name
            FROM Health_record
            WHERE Dog_ID = ?
            ORDER BY Administered_Date DESC, Record_ID DESC
            """,
            (dog_id,),
        ).fetchall()
        return [HealthRecord(row) for row in rows]

    @staticmethod
    def create(dog_id, administered_date, vaccine_name):
        """Create a health record and return the new object."""
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO Health_record (Dog_ID, Administered_Date, Vaccine_Name)
            VALUES (?, ?, ?)
            """,
            (dog_id, administered_date, vaccine_name),
        )
        db.commit()
        return HealthRecord.get_by_id(cursor.lastrowid)

    @staticmethod
    def update(record_id, administered_date, vaccine_name):
        """Update a health record and return the updated object."""
        db = get_db()
        db.execute(
            """
            UPDATE Health_record
            SET Administered_Date = ?, Vaccine_Name = ?
            WHERE Record_ID = ?
            """,
            (administered_date, vaccine_name, record_id),
        )
        db.commit()
        return HealthRecord.get_by_id(record_id)

    @staticmethod
    def delete(record_id):
        """Delete a health record by ID and return whether it existed."""
        db = get_db()
        cursor = db.execute(
            """
            DELETE FROM Health_record
            WHERE Record_ID = ?
            """,
            (record_id,),
        )
        db.commit()
        return cursor.rowcount > 0
