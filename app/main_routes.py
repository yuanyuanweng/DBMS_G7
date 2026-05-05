"""
Landing page route

TODO:
- Import Dog model from app/models.
- Query/filter dogs based on request parameters.
- Pass the filtered dog list to index.html.
"""
from flask import Blueprint, render_template 


main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Render the landing page with dog data."""
    
    return render_template('index.html', dogs=None)
    
    
    