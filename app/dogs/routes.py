"""
Dog-related routes.

Current progress:
- Dog list/detail use real database data through the Dog model.
- Dog create/edit are admin-only and save uploaded images, short descriptions,
  and health status records.
- Availability is derived from application status through Dog_With_Status.
"""

import os
from datetime import date
from uuid import uuid4

from flask import Blueprint, render_template, request, abort, redirect, session, url_for, flash, jsonify, current_app
from werkzeug.utils import secure_filename
from app.auth.utils import admin_required
from app.database import get_db
from app.models.dog import Dog
from app.models.application import Application
from app.models.health_record import HealthRecord
from app.models.shelter import Shelter

dogs_bp = Blueprint("dogs", __name__)


GENDER_MAP = {
    "male": "Male",
    "female": "Female",
    "brother": "Male",
    "sister": "Female",
    "boy": "Male",
    "girl": "Female",
    "弟弟": "Male",
    "妹妹": "Female",
}

AGE_GROUP_MAP = {
    "puppy": "puppy",
    "young": "young",
    "adult": "adult",
    "senior": "senior",
    "0-1": "puppy",
    "1-3": "young",
    "3-8": "adult",
    "8+": "senior",
}

SIZE_MAP = {
    "small": "Small",
    "medium": "Medium",
    "large": "Large",
    "under_12": "Small",
    "12_25": "Medium",
    "25_plus": "Large",
}

SORT_MAP = {
    "latest": "newest",
    "newest": "newest",
    "oldest": "oldest",
    "age_asc": "age_asc",
    "age_desc": "age_desc",
}

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


class FormField:
    """Template helper for form.field.data."""

    def __init__(self, data=""):
        self.data = data


class DogFormView:
    """Template helper for create/edit form state."""

    FIELD_NAMES = (
        "name", "breed", "age", "gender", "health_status",
        "shelter_id", "description",
    )

    def __init__(self, form_data=None, errors=None):
        self.errors = errors or {}
        form_data = form_data or {}

        for field_name in self.FIELD_NAMES:
            value = form_data.get(field_name, "")
            if field_name == "is_urgent":
                value = bool(value)
            setattr(self, field_name, FormField(value))


def _first_arg(*names, default=""):
    """Return the first non-empty query parameter."""
    for name in names:
        value = request.args.get(name, "").strip()
        if value:
            return value
    return default


def _normalize(value, mapping, default=""):
    """Normalize filter values for Dog.search."""
    if not value:
        return default
    return mapping.get(value.lower(), value)


def _parse_age(value):
    """Extract integer age from form text."""
    value = (value or "").strip()
    digits = "".join(char for char in value if char.isdigit())
    return int(digits) if digits else 0


def _save_uploaded_image(file_storage):
    """Save an uploaded dog image and return its static URL path."""
    if not file_storage or not file_storage.filename:
        return None

    filename = secure_filename(file_storage.filename)
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return None

    upload_dir = os.path.join(current_app.root_path, "static", "img", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    saved_name = f"{uuid4().hex}.{extension}"
    file_storage.save(os.path.join(upload_dir, saved_name))
    return f"/static/img/uploads/{saved_name}"


@dogs_bp.route("/find-a-dog/", methods=["GET"])
def list_dogs():
    """Render searchable dog listing page."""

    q = _first_arg("q", "search", "keyword")
    gender = _normalize(_first_arg("gender", "sex"), GENDER_MAP)
    age_group = _normalize(_first_arg("age_group", "age"), AGE_GROUP_MAP)
    size = _normalize(_first_arg("size", "weight_group", "weight"), SIZE_MAP)
    city = _first_arg("city")
    good_with = _first_arg("good_with")
    sort = _normalize(_first_arg("sort", default="newest"), SORT_MAP, "newest")

    dogs = Dog.search(
        q=q,
        gender=gender,
        age_group=age_group,
        size=size,
        city=city,
        sort=sort,
    )

    filters = {
        "q": q,
        "gender": gender,
        "age_group": age_group,
        "size": size,
        "city": city,
        "good_with": good_with,
        "sort": sort,
    }

    stats = {
        "total": len(dogs),
        "available": len([dog for dog in dogs if dog.availability == "Available"]),
        "pending": len([dog for dog in dogs if dog.availability == "Pending"]),
        "adopted": len([dog for dog in dogs if dog.availability == "Adopted"]),
        "urgent": len([dog for dog in dogs if dog.is_urgent]),
    }

    user_id = session.get('user_id')
    liked_ids = set()
    favorite_dogs = []
    if user_id:
        db = get_db()
        rows = db.execute(
            'SELECT Dog_ID FROM Favorite WHERE User_ID = ? ORDER BY Created_at DESC', (user_id,)
        ).fetchall()
        liked_ids = {row['Dog_ID'] for row in rows}
        favorite_dogs = [Dog.get_by_id(row['Dog_ID']) for row in rows]
        favorite_dogs = [d for d in favorite_dogs if d]

    return render_template(
        "dogs/list.html",
        dogs=dogs,
        dogs_json=[dog.to_dict() for dog in dogs],
        filters=filters,
        stats=stats,
        liked_ids=liked_ids,
        favorite_dogs=favorite_dogs,
    )


@dogs_bp.route("/find-a-dog/<int:dog_id>", methods=["GET"])
def dog_detail(dog_id):
    """Render one dog profile page."""
    
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


def dog_detail_alias(id):
    """Support old templates that use id=..."""
    return dog_detail(id)


dogs_bp.add_url_rule("/find-a-dog/", endpoint="list", view_func=list_dogs)
dogs_bp.add_url_rule("/find-a-dog/<int:id>", endpoint="detail", view_func=dog_detail_alias)

@dogs_bp.route("/shelter/create_dog", methods=["GET", "POST"])
@admin_required
def create():
    """Render and handle admin dog creation."""

    form = DogFormView(request.form if request.method == "POST" else None)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        breed = request.form.get("breed", "").strip()
        gender = request.form.get("gender", "").strip() or "Unknown"
        shelter_id = request.form.get("shelter_id", "").strip()
        age = _parse_age(request.form.get("age", ""))
        description = request.form.get("description", "").strip() or None
        health_status = request.form.get("health_status", "").strip()
        image_url = _save_uploaded_image(request.files.get("image"))

        errors = {}
        if not name:
            errors.setdefault("name", []).append("Name is required.")
        if not breed:
            errors.setdefault("breed", []).append("Breed is required.")
        if not shelter_id:
            errors.setdefault("shelter_id", []).append("Shelter is required.")

        if not errors:
            dog_id = Dog.create(
                shelter_id=int(shelter_id),
                name=name,
                gender=gender,
                age=age,
                breed=breed,
                image_url=image_url,
                description=description,
            )
            if health_status:
                HealthRecord.create(dog_id, date.today().isoformat(), health_status)
            flash("Dog profile created.", "success")
            return redirect(url_for("admin.dashboard"))

        form = DogFormView(request.form, errors)

    shelters = Shelter.get_all()

    return render_template(
        "dogs/create.html",
        shelters=shelters,
        form=form,
        csrf_token=lambda: "",
    )

@dogs_bp.route("/shelter/<int:id>/edit_dog", methods=["GET", "POST"])
@admin_required
def edit(id):
    """Render and handle admin dog editing."""
    
    dog = Dog.get_by_id(id)

    if dog is None:
        abort(404)

    form = DogFormView()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        breed = request.form.get("breed", "").strip()
        gender = request.form.get("gender", "").strip() or "Unknown"
        shelter_id = request.form.get("shelter_id", "").strip()
        age = _parse_age(request.form.get("age", ""))
        description = request.form.get("description", "").strip() or None
        health_status = request.form.get("health_status", "").strip()
        image_url = _save_uploaded_image(request.files.get("image")) or dog.image_url

        errors = {}
        if not name:
            errors.setdefault("name", []).append("Name is required.")
        if not breed:
            errors.setdefault("breed", []).append("Breed is required.")
        if not shelter_id:
            errors.setdefault("shelter_id", []).append("Shelter is required.")

        if not errors:
            Dog.update(
                dog_id=id,
                shelter_id=int(shelter_id),
                name=name,
                gender=gender,
                age=age,
                breed=breed,
                image_url=image_url,
                description=description,
            )
            if health_status and health_status != dog.health_status:
                HealthRecord.create(id, date.today().isoformat(), health_status)
            flash("Dog profile updated.", "success")
            return redirect(url_for("admin.dashboard"))

        form = DogFormView(request.form, errors)

    shelters = Shelter.get_all()

    return render_template(
        "dogs/edit.html",
        dog=dog,
        shelters=shelters,
        form=form,
        csrf_token=lambda: "",
    )


@dogs_bp.route("/dogs/<int:dog_id>/like", methods=["POST"])
def toggle_like(dog_id):
    """Toggle favorite status for a dog. Returns JSON {liked: bool}."""
    if not session.get('user_id'):
        return jsonify({'error': 'login required'}), 401
    user_id = session['user_id']
    db = get_db()
    existing = db.execute(
        'SELECT 1 FROM Favorite WHERE User_ID = ? AND Dog_ID = ?',
        (user_id, dog_id)
    ).fetchone()
    if existing:
        db.execute('DELETE FROM Favorite WHERE User_ID = ? AND Dog_ID = ?', (user_id, dog_id))
        liked = False
    else:
        db.execute('INSERT INTO Favorite (User_ID, Dog_ID) VALUES (?, ?)', (user_id, dog_id))
        liked = True
    db.commit()
    return jsonify({'liked': liked})
