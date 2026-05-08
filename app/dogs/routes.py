"""
Dog-related routes.

- Use mock dog data from app/models/dog.py.
- Keep routes simple until database schema and dogs/list.html are ready.
- Dog details are displayed by frontend popup/modal, not a separate page.
"""

from flask import Blueprint, render_template
from app.models.dog import Dog

dogs_bp = Blueprint("dogs", __name__, url_prefix="/dogs")

#URL: http://127.0.0.1:5000/dogs
@dogs_bp.route("/")
def dog_list():
    """
    Render the dog listing page.
    """
    dogs = Dog.get_all()
    return render_template("dogs/list.html", dogs=dogs)