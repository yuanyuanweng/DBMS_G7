from flask import Blueprint, request, jsonify, session
from app.models.dog import Dog
from app.ai.story_generator import generate_story, match_dogs

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/ai/story/<int:dog_id>", methods=["POST"])
def story(dog_id):
    dog = Dog.get_by_id(dog_id)
    if not dog:
        return jsonify({"error": "Dog not found"}), 404

    try:
        text = generate_story(dog)
        return jsonify({"story": text})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Story generation failed."}), 500


@ai_bp.route("/ai/match", methods=["POST"])
def match():
    data = request.get_json(silent=True) or {}
    query = (data.get("query") or "").strip()
    if not query:
        return jsonify({"error": "Query is required"}), 400

    dogs = Dog.get_all()
    dogs_data = [d.to_dict() for d in dogs]

    try:
        recommendations = match_dogs(query, dogs_data)
        return jsonify({"recommendations": recommendations})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "AI matching failed."}), 500
