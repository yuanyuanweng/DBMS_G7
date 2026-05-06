'''
Landing page route.

Current approach:
- Show only 6 dogs on index.html.
- Use mock data from Dog model.

TODO:
- Replace mock data with SQL through models/dog.py after schema is ready.
'''

from flask import Blueprint, render_template 
from app.models.dog import Dog

main = Blueprint('main', __name__)

@main.route('/')
def index():
    '''
    Render homepage with a small dog preview.
    '''
    dogs = Dog.get_featured(limit=4)

    return render_template('index.html', dogs=dogs)
    
    
    