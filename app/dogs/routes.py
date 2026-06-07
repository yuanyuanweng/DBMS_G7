"""
Dog-related routes.

- Public dog browsing pages use the Dog model, which reads from SQLite.
- The list page passes stable filter state to dogs/list.html.
- The detail page checks whether the logged-in user has already applied.
- Shelter create/edit pages save only fields that exist in the current schema.

Current schema limitation:
- Frontend-only fields such as exact weight, "good with", city, urgent flag,
  description, and health notes are accepted for template compatibility, but
  they cannot be fully stored or filtered until the Dog schema adds columns.
"""

from flask import Blueprint, render_template, request, abort, redirect, session, url_for, flash, jsonify
from app.database import get_db
from app.models.dog import Dog
from app.models.application import Application
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


class FormField:
    """Minimal helper so templates can read form.field.data."""

    def __init__(self, data=""):
        self.data = data


class DogFormView:
    """Minimal form object used by current create/edit templates."""

    FIELD_NAMES = (
        "name", "breed", "age", "gender", "size", "city", "health_status",
        "is_urgent", "shelter_id", "description",
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
    """Return the first non-empty query parameter from supported aliases."""
    for name in names:
        value = request.args.get(name, "").strip()
        if value:
            return value
    return default


def _normalize(value, mapping, default=""):
    """Map frontend filter values into the values used by the Dog model."""
    if not value:
        return default
    return mapping.get(value.lower(), value)


def _parse_age(value):
    """Extract an integer age from text such as '2 years'."""
    value = (value or "").strip()
    digits = "".join(char for char in value if char.isdigit())
    return int(digits) if digits else 0


# Dog listing page.
@dogs_bp.route("/find-a-dog/", methods=["GET"])
def list_dogs():
    """
    Render the dog listing page.

    Supported query parameters for frontend:
    - q / search / keyword: search by dog name or breed
    - gender / sex: Male, Female, brother, sister, boy, girl
    - age_group / age: puppy, young, adult, senior
    - size / weight_group: Small, Medium, Large
    - city: city filter derived from shelter location/name
    - good_with: kept in filter state, not applied until DB has this data
    - sort: newest/latest, oldest, age_asc, age_desc
    """

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

    # Preserve active filter values for the template.
    filters = {
        "q": q,
        "gender": gender,
        "age_group": age_group,
        "size": size,
        "city": city,
        "good_with": good_with,
        "sort": sort,
    }

    # Summary counts for the list page header/filter UI.
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


# Dog detail page.
@dogs_bp.route("/find-a-dog/<int:dog_id>", methods=["GET"])
def dog_detail(dog_id):
    """Render one dog profile and application status for the current user."""
    
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
    """Compatibility endpoint for templates that pass id=..."""
    return dog_detail(id)


# Compatibility endpoints for older templates.
dogs_bp.add_url_rule("/find-a-dog/", endpoint="list", view_func=list_dogs)
dogs_bp.add_url_rule("/find-a-dog/<int:id>", endpoint="detail", view_func=dog_detail_alias)

# Shelter dog creation page.
@dogs_bp.route("/shelter/create_dog", methods=["GET", "POST"])
def create():
    """
    Render and handle the create dog form.

    Current schema-backed fields:
    - Shelter_ID, Name, Gender, Age, Breed, Image_URL

    Frontend-only fields such as size, city, urgent, description, and health notes
    are accepted by the form but not saved until the Dog schema supports them.
    """

    form = DogFormView(request.form if request.method == "POST" else None)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        breed = request.form.get("breed", "").strip()
        gender = request.form.get("gender", "").strip() or "Unknown"
        shelter_id = request.form.get("shelter_id", "").strip()
        age = _parse_age(request.form.get("age", ""))
        image_url = request.form.get("image_url", "").strip() or None

        errors = {}
        if not name:
            errors.setdefault("name", []).append("Name is required.")
        if not breed:
            errors.setdefault("breed", []).append("Breed is required.")
        if not shelter_id:
            errors.setdefault("shelter_id", []).append("Shelter is required.")

        if not errors:
            db = get_db()
            cursor = db.execute(
                """
                INSERT INTO Dog (Shelter_ID, Name, Gender, Age, Breed, Image_URL)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (int(shelter_id), name, gender, age, breed, image_url),
            )
            db.commit()
            flash("Dog profile created.", "success")
            return redirect(url_for("dogs.dog_detail", dog_id=cursor.lastrowid))

        form = DogFormView(request.form, errors)

    shelters = Shelter.get_all()

    # GET shows an empty form; POST with errors re-renders the submitted data.
    return render_template(
        "dogs/create.html",
        shelters=shelters,
        form=form,
        csrf_token=lambda: "",
    )

# Shelter dog edit page.
@dogs_bp.route("/shelter/<int:id>/edit_dog", methods=["GET", "POST"])
def edit(id):
    """
    Render and handle the edit dog form.

    Only current Dog table columns are updated. Template-only fields such as
    size, city, urgent flag, description, and health notes are displayed for
    frontend compatibility but are not persisted by this route yet.
    """
    
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
        image_url = request.form.get("image_url", "").strip() or dog.image_url

        errors = {}
        if not name:
            errors.setdefault("name", []).append("Name is required.")
        if not breed:
            errors.setdefault("breed", []).append("Breed is required.")
        if not shelter_id:
            errors.setdefault("shelter_id", []).append("Shelter is required.")

        if not errors:
            db = get_db()
            db.execute(
                """
                UPDATE Dog
                SET Shelter_ID = ?, Name = ?, Gender = ?, Age = ?, Breed = ?, Image_URL = ?
                WHERE Dog_ID = ?
                """,
                (int(shelter_id), name, gender, age, breed, image_url, id),
            )
            db.commit()
            flash("Dog profile updated.", "success")
            return redirect(url_for("dogs.dog_detail", dog_id=id))

        form = DogFormView(request.form, errors)

    shelters = Shelter.get_all()

    # GET shows the current dog values; POST with errors re-renders them.
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
