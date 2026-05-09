'''
Landing page route.

Current approach:
- Show only 4 dogs on index.html.
- Use mock data from Dog model. (Dog.get_featured())
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
    
    
    