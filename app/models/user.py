from app.database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, row):
        self.id = row['User_ID']
        self.email = row['Email']
        self.role = 'admin' if row['Role'] == 1 else 'user'

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        row = db.execute('SELECT * FROM Users WHERE User_ID = ?', (user_id,)).fetchone()
        return User(row) if row else None

    @staticmethod
    def verify_password(email, password):
        db = get_db()
        row = db.execute('SELECT * FROM Users WHERE Email = ?', (email,)).fetchone()
        if row and check_password_hash(row['Password_Hash'], password):
            return User(row)
        return None

    @staticmethod
    def create(email, password):
        db = get_db()
        try:
            db.execute(
                'INSERT INTO Users (Role, Email, Password_Hash) VALUES (0, ?, ?)',
                (email, generate_password_hash(password))
            )
            db.commit()
            return True, None
        except Exception as e:
            return False, str(e)
