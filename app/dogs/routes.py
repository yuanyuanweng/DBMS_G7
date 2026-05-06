'''
Dog-related routes.

Current approach:
- Use mock dog data from app/models/dog.py.
- Keep routes simple until database schema is ready.

TODO:
- Add search/filter later.
- Add pagination later if needed.
- Replace mock data with SQL through models/dog.py after schema is ready.
'''

from flask import Blueprint, render_template, abort
from app.models.dog import Dog

dogs_bp = Blueprint('dogs', __name__, url_prefix='/dogs')

# URL: xxx/dogs/
@dogs_bp.route('/')
def list_dogs():
    '''
    Render page showing all dogs.
    '''
    dogs = Dog.get_all()

    return render_template('dogs/list.html', dogs=dogs)

# URL: xxx/dogs/<dog_id>
@dogs_bp.route('/<int:dog_id>')
def dog_detail(dog_id):
    '''
    Render detail page for one dog.
    '''
    dog = Dog.get_by_id(dog_id)

    if dog is None:
        abort(404)
        
    return render_template('dogs/detail.html', dog=dog)
