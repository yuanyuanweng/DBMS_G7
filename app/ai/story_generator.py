import json
import os
from urllib.error import URLError
from urllib.request import Request, urlopen

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def _build_prompt(dog):
    shelter_name = dog.shelter.name if dog.shelter else "Unknown shelter"
    health_status = dog.health_status or "Ask the shelter for details"
    description = dog.desc or "No extra description provided"

    return f"""
Write a warm adoption story for this dog.

Dog profile:
- Name: {dog.name}
- Breed: {dog.breed}
- Age: {dog.age}
- Gender: {dog.gender}
- Size: {dog.size}
- Shelter: {shelter_name}
- Health: {health_status}
- Description: {description}

Requirements:
- Around 80 words.
- Friendly, hopeful, and suitable for an adoption website.
- Write from the dog's point of view.
- Do not invent medical facts or guaranteed behavior.
"""


def _fallback_story(dog):
    shelter_name = dog.shelter.name if dog.shelter else "the shelter"
    return (
        f"Hi, I'm {dog.name}. I am a {dog.age} {dog.breed} waiting at "
        f"{shelter_name}. I may need time, patience, and a kind home, but I "
        "have a lot of love to give. If you think we could be a good match, "
        "please ask the shelter more about me."
    )


def generate_dog_story(dog):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": _build_prompt(dog),
        "stream": False,
        "options": {
            "temperature": 0.8,
            "num_predict": 140,
        },
    }

    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
            story = (data.get("response") or "").strip()
            return story or _fallback_story(dog)
    except (OSError, URLError, json.JSONDecodeError):
        return _fallback_story(dog)
