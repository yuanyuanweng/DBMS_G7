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
    def get_admin_counts():
        """Return dashboard counts for admin application summary."""
        db = get_db()
        return {
            "pending_count": db.execute(
                "SELECT COUNT(*) FROM Application WHERE Status = ?",
                (STATUS_PENDING,),
            ).fetchone()[0],
            "approved_count": db.execute(
                "SELECT COUNT(*) FROM Application WHERE Status = ?",
                (STATUS_APPROVED,),
            ).fetchone()[0],
            "rejected_count": db.execute(
                "SELECT COUNT(*) FROM Application WHERE Status = ?",
                (STATUS_REJECTED,),
            ).fetchone()[0],
        }

    @staticmethod
    def get_recent_for_admin(limit=20):
        """Return recent application rows for the admin dashboard."""
        db = get_db()
        return db.execute(
            """
            SELECT a.App_ID, a.Status, a.Created_at,
                   u.Email, u.User_ID,
                   d.Name AS Dog_Name, d.Dog_ID
            FROM Application a
            JOIN Users u ON a.User_ID = u.User_ID
            JOIN Dog d ON a.Dog_ID = d.Dog_ID
            ORDER BY a.Created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    @staticmethod
    def get_admin_users():
        """Return user rows displayed on the admin dashboard."""
        db = get_db()
        return db.execute(
            "SELECT User_ID, Email, Role FROM Users ORDER BY User_ID DESC"
        ).fetchall()

    @staticmethod
    def count_users():
        """Return total user count for the admin dashboard."""
        db = get_db()
        return db.execute("SELECT COUNT(*) FROM Users").fetchone()[0]

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
        """Update an application's status.If one application is approved, reject all other applications
        for the same dog to prevent multiple adopters from being approved.
        """
        if status not in VALID_STATUSES:
            return False, "Invalid status."

        db = get_db()

        application = db.execute(
            """
            SELECT App_ID, Dog_ID
            FROM Application
            WHERE App_ID = ?
            """,
            (app_id,),
        ).fetchone()

        if application is None:
            return False, "Application not found."

        dog_id = application["Dog_ID"]

        db.execute(
            """
            UPDATE Application
            SET Status = ?
            WHERE App_ID = ?
            """,
            (status, app_id),
        )

        if status == 1:
            db.execute(
                """
                UPDATE Application
                SET Status = 2
                WHERE Dog_ID = ?
                  AND App_ID != ?
                  AND Status IN (0, 1)
                """,
                (dog_id, app_id),
            )
        db.commit()
        return True, Application.get_by_id(app_id)
    
    @staticmethod
    def delete_by_id(app_id):
        """Delete one application by ID."""
        db = get_db()
        cursor = db.execute(
            """
            DELETE FROM Application
            WHERE App_ID = ?
            """,
            (app_id,),
        )
        db.commit()
        return cursor.rowcount > 0
