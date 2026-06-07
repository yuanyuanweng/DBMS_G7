'''
Landing page route.
'''

from flask import Blueprint, render_template, session
from app.models.dog import Dog
from app.database import get_db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    dogs = Dog.get_featured(limit=4)

    liked_ids = set()
    user_id = session.get('user_id')
    if user_id:
        db = get_db()
        rows = db.execute(
            'SELECT Dog_ID FROM Favorite WHERE User_ID = ?', (user_id,)
        ).fetchall()
        liked_ids = {row['Dog_ID'] for row in rows}

    return render_template('index.html', dogs=dogs, liked_ids=liked_ids)
    
    
    