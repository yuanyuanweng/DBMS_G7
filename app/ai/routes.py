from flask import Blueprint, jsonify, request
from app.models.dog import Dog
from app.ai.story_generator import generate_dog_story

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")


def _score_dog_for_query(dog, query):
    """Return a simple local match score and explanation for one dog."""
    text = query.lower()
    score = 0
    reasons = []

    dog_text = " ".join(
        str(value).lower()
        for value in (
            dog.name,
            dog.breed,
            dog.gender,
            dog.age,
            dog.city,
            dog.size,
            dog.description,
            " ".join(dog.tags),
        )
        if value
    )

    for word in text.split():
        if len(word) >= 3 and word in dog_text:
            score += 2

    if any(word in text for word in ("apartment", "small", "quiet", "calm")):
        if dog.size == "Small" or dog.raw_age >= 8:
            score += 3
            reasons.append("may fit a quieter or smaller living space")

    if any(word in text for word in ("active", "run", "running", "hike", "outdoor")):
        if dog.raw_age < 8 and dog.size in ("Medium", "Large"):
            score += 3
            reasons.append("could be a good match for an active lifestyle")

    if any(word in text for word in ("puppy", "young", "playful")):
        if dog.raw_age < 3:
            score += 3
            reasons.append("matches your interest in a younger dog")

    if any(word in text for word in ("senior", "older", "gentle")):
        if dog.raw_age >= 8:
            score += 3
            reasons.append("matches your interest in a calmer senior dog")

    if not reasons:
        reasons.append(
            f"{dog.name}'s profile has traits that may fit what you described"
        )

    return score, "; ".join(reasons).capitalize() + "."

@ai_bp.route("/story/<int:dog_id>", methods=["POST"])
def story(dog_id):
    dog = Dog.get_by_id(dog_id)
    if not dog:
        return jsonify({"error": "Dog not found"}), 404

    story_text = generate_dog_story(dog)
    return jsonify({"story": story_text})


@ai_bp.route("/match", methods=["POST"])
def match():
    data = request.get_json(silent=True) or {}
    query = (data.get("query") or "").strip()

    if not query:
        return jsonify({"recommendations": []}), 400

    ranked = []
    for dog in Dog.get_all():
        score, reason = _score_dog_for_query(dog, query)
        ranked.append((score, dog, reason))

    ranked.sort(key=lambda item: (item[0], item[1].id), reverse=True)
    recommendations = [
        {"id": dog.id, "reason": reason}
        for score, dog, reason in ranked[:3]
        if score > 0
    ]

    if not recommendations:
        recommendations = [
            {
                "id": dog.id,
                "reason": f"{dog.name} could still be worth meeting based on the available profile.",
            }
            for dog in Dog.get_all()[:3]
        ]

    return jsonify({"recommendations": recommendations})
