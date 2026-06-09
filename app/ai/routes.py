from flask import Blueprint, jsonify
from app.models.dog import Dog
from app.ai.story_generator import generate_dog_story

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")


@ai_bp.route("/story/<int:dog_id>", methods=["POST"])
def story(dog_id):
    dog = Dog.get_by_id(dog_id)
    if not dog:
        return jsonify({"error": "Dog not found"}), 404

    story_text = generate_dog_story(dog)
    return jsonify({"story": story_text})
