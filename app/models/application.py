from app.database import get_db
from app.models.dog import Dog

STATUS_PENDING = 0
STATUS_APPROVED = 1
STATUS_REJECTED = 2

STATUS_MAP = {
    STATUS_PENDING: "Pending",
    STATUS_APPROVED: "Approved",
    STATUS_REJECTED: "Rejected",
}

VALID_STATUSES = tuple(STATUS_MAP.keys())


class Application:
    def __init__(self, row):
        """Create an Application object from one database row."""
        self.id = row["App_ID"]
        self.user_id = row["User_ID"]
        self.dog_id = row["Dog_ID"]
        self.status_code = row["Status"]
        self.status = STATUS_MAP.get(self.status_code, "Pending")
        self.match_score = row["Match_Score"]
        self.created_at = row["Created_at"] or ""
        self.dog = Dog.get_by_id(self.dog_id)

    def to_dict(self):
        """Convert the application object into a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "dog_id": self.dog_id,
            "status_code": self.status_code,
            "status": self.status,
            "match_score": self.match_score,
            "created_at": self.created_at,
        }

    @staticmethod
    def get_by_id(app_id):
        """Return one application by its application ID."""
        db = get_db()
        row = db.execute(
            """
            SELECT App_ID, User_ID, Dog_ID, Status, Match_Score, Created_at
            FROM Application
            WHERE App_ID = ?
            """,
            (app_id,),
        ).fetchone()
        return Application(row) if row else None

    @staticmethod
    def get_by_user(user_id):
        """Return all applications submitted by one user."""
        db = get_db()
        rows = db.execute(
            """
            SELECT App_ID, User_ID, Dog_ID, Status, Match_Score, Created_at
            FROM Application
            WHERE User_ID = ?
            ORDER BY Created_at DESC
            """,
            (user_id,),
        ).fetchall()
        return [Application(row) for row in rows]

    @staticmethod
    def already_applied(user_id, dog_id):
        """Return whether a user already applied for one dog."""
        db = get_db()
        row = db.execute(
            """
            SELECT App_ID
            FROM Application
            WHERE User_ID = ? AND Dog_ID = ?
            """,
            (user_id, dog_id),
        ).fetchone()
        return row is not None

    @staticmethod
    def create(user_id, dog_id, match_score=None):
        """Create a pending application for one user and dog."""
        db = get_db()
        try:
            cursor = db.execute(
                """
                INSERT INTO Application (User_ID, Dog_ID, Status, Match_Score)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, dog_id, STATUS_PENDING, match_score),
            )
            db.commit()
            return True, cursor.lastrowid
        except Exception as e:
            return False, str(e)

    @staticmethod
    def cancel(app_id, user_id):
        """Cancel a pending application belonging to one user."""
        db = get_db()
        cursor = db.execute(
            """
            DELETE FROM Application
            WHERE App_ID = ? AND User_ID = ? AND Status = ?
            """,
            (app_id, user_id, STATUS_PENDING),
        )
        db.commit()
        return cursor.rowcount > 0

    @staticmethod
    def update_status(app_id, status):
        """Update an application's status and return the updated object."""
        if status not in VALID_STATUSES:
            return False, "Invalid status."

        db = get_db()
        cursor = db.execute(
            """
            UPDATE Application
            SET Status = ?
            WHERE App_ID = ?
            """,
            (status, app_id),
        )
        db.commit()
        if cursor.rowcount == 0:
            return False, "Application not found."
        return True, Application.get_by_id(app_id)
