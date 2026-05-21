from app.database import get_db
from app.models.dog import Dog

STATUS_MAP = {0: 'Pending', 1: 'Approved', 2: 'Rejected'}

class Application:
    def __init__(self, row):
        self.id = row['App_ID']
        self.user_id = row['User_ID']
        self.dog_id = row['Dog_ID']
        self.status = STATUS_MAP.get(row['Status'], 'Pending')
        self.created_at = row['Created_at'] or ''
        self.dog = Dog.get_by_id(self.dog_id)

    @staticmethod
    def get_by_user(user_id):
        db = get_db()
        rows = db.execute(
            'SELECT * FROM Application WHERE User_ID = ? ORDER BY Created_at DESC',
            (user_id,)
        ).fetchall()
        return [Application(row) for row in rows]

    @staticmethod
    def already_applied(user_id, dog_id):
        db = get_db()
        row = db.execute(
            'SELECT App_ID FROM Application WHERE User_ID = ? AND Dog_ID = ?',
            (user_id, dog_id)
        ).fetchone()
        return row is not None

    @staticmethod
    def create(user_id, dog_id):
        db = get_db()
        try:
            db.execute(
                'INSERT INTO Application (User_ID, Dog_ID, Status) VALUES (?, ?, 0)',
                (user_id, dog_id)
            )
            db.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    @staticmethod
    def cancel(app_id, user_id):
        db = get_db()
        db.execute(
            'DELETE FROM Application WHERE App_ID = ? AND User_ID = ?',
            (app_id, user_id)
        )
        db.commit()
