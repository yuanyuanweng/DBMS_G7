"""
Dog-related routes.

- Use mock dog data from app/models/dog.py.
- Keep routes simple until database schema and dogs/list.html are ready.
- Dog list is displayed in dogs/list.html.
- Dog details are displayed in dogs/detail.html.

TODO:
1) already_applied未來會修改
2) redirect(url_for("blueprint.function")): 提交Form後, 把user送回要去的網址
"""

from flask import Blueprint, render_template, request, abort, redirect, session
from app.models.dog import Dog
from app.models.application import Application
from app.models.shelter import Shelter

dogs_bp = Blueprint("dogs", __name__)

#URL: http://127.0.0.1:5000/find-a-dog
@dogs_bp.route("/find-a-dog/", methods=["GET"])
def list_dogs():
    '''
    Render the dog listing page.
    
    - Provide dog list data to templates/dogs/list.html
    
    Supported URL parameters: (暫定 可修改)
    - q: search by dog name or breed
    - gender: Male / Female 
    - age_group: puppy / young / adult / senior 
    - size: Small / Medium / Large 
    - city: Taipei / New Taipei / Taichung / Tainan / Kaohsiung 
    - sort: newest / oldest / age_asc / age_desc
    '''
    
    # Basic query parameters for frontend filters (前端目前可用的)
    q = request.args.get("q", "").strip()
    gender = request.args.get("gender", "")
    age_group = request.args.get("age_group", "")
    size = request.args.get("size", "")
    city = request.args.get("city", "")
    sort = request.args.get("sort", "newest")
    
    dogs = Dog.search(
        q=q,
        gender=gender,
        age_group=age_group,
        size=size,
        city=city,
        sort=sort
    )
    
    # Keep current filter values available during one request cycle 
    filters = {
        "q": q,
        "gender": gender, 
        "age_group": age_group,
        "size": size, 
        "city": city,
        "sort": sort 
    }
    
    # Shows the summary 統計數字
    stats = {
        "total": len(dogs),
        "available": len([dog for dog in dogs if dog.availability == "Available"]),
        "urgent": len([dog for dog in dogs if dog.is_urgent])
    }
    
    return render_template(
        "dogs/list.html", 
        dogs=dogs, # list(dict()), for HTML/Jinja2
        dogs_json=[dog.to_dict() for dog in dogs], # jsonify(), for Javascript
        filters=filters,
        stats=stats
        # liked_ids 可加可不加 
    )
    
# URL: http://127.0.0.1:5000/find-a-dog/<dog_id>
@dogs_bp.route("/find-a-dog/<int:dog_id>", methods=["GET"])
def dog_detail(dog_id):
    '''
    Render detail page for one dog
    '''
    
    dog = Dog.get_by_id(dog_id)
    
    if dog is None: 
        abort(404)
    
    user_id = session.get('user_id')
    already_applied = Application.already_applied(user_id, dog_id) if user_id else False

    return render_template(
        "dogs/detail.html",
        dog=dog,
        dog_json=dog.to_dict(),
        already_applied=already_applied
    )

# http://127.0.0.1:5000/shelter/create_dog
@dogs_bp.route("/shelter/create_dog", methods=["GET", "POST"])
def create():
    '''
    Render the create dog page. (For Shelter Admins only)
    
    Temporary:
    - Use mock shelter data.
    - Real POST handling and database insert will be added when database & frontend is stable
    '''
    
    # TODO
    if request.method == "POST":
        # read form data
        # INSERT INTO Dog ...
        # redirect after success
        pass

    shelters = Shelter.get_all()

    # GET req: shows empty form
    return render_template(
        "dogs/create.html",
        shelters=shelters
    )

# http://127.0.0.1:5000/shelter/<int:dog_id>/edit_dog
@dogs_bp.route("/shelter/<int:dog_id>/edit_dog", methods=["GET", "POST"])
def edit(dog_id):
    '''
    Render and handle the edit dog page (For Shelter Admins only)
    
    Temporary:
    - Uses mock dog data from Dog.get_by_id()
    - Uses mock shelter data
    - Real POST handling and database update will be added when database and frontend is stable
    '''
    
    dog = Dog.get_by_id(dog_id)

    if dog is None:
        abort(404)
    
    # TODO
    if request.method == "POST":
        # read form data
        # UPDATE Dog SET ... WHERE Dog_ID = ?
        # redirect after success
        pass

    shelters = Shelter.get_all()

    # GET req: shows filled form with that specific id
    return render_template(
        "dogs/edit.html",
        dog=dog,
        shelters=shelters
    )
