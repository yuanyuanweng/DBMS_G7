from app.database import get_db
from app.models.dog import Dog


class Favorite:
    """Favorite dog records for one user."""

    @staticmethod
    def get_user_favorite_ids(user_id):
        """Return dog IDs favorited by one user, newest first."""
        db = get_db()
        rows = db.execute(
            """
            SELECT Dog_ID
            FROM Favorite
            WHERE User_ID = ?
            ORDER BY Created_at DESC
            """,
            (user_id,),
        ).fetchall()
        return [row["Dog_ID"] for row in rows]

    @staticmethod
    def get_user_favorite_dogs(user_id):
        """Return Dog objects favorited by one user, newest first."""
        dog_ids = Favorite.get_user_favorite_ids(user_id)
        dogs = [Dog.get_by_id(dog_id) for dog_id in dog_ids]
        return [dog for dog in dogs if dog]

    @staticmethod
    def is_favorited(user_id, dog_id):
        """Return whether a user has favorited one dog."""
        db = get_db()
        row = db.execute(
            """
            SELECT 1
            FROM Favorite
            WHERE User_ID = ? AND Dog_ID = ?
            """,
            (user_id, dog_id),
        ).fetchone()
        return row is not None

    @staticmethod
    def toggle(user_id, dog_id):
        """Toggle one favorite row and return the new liked state."""
        db = get_db()

        if Favorite.is_favorited(user_id, dog_id):
            db.execute(
                """
                DELETE FROM Favorite
                WHERE User_ID = ? AND Dog_ID = ?
                """,
                (user_id, dog_id),
            )
            liked = False
        else:
            db.execute(
                """
                INSERT INTO Favorite (User_ID, Dog_ID)
                VALUES (?, ?)
                """,
                (user_id, dog_id),
            )
            liked = True

        db.commit()
        return liked
