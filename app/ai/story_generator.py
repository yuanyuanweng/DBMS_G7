import os
import json
from openai import OpenAI

_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set.")
        _client = OpenAI(api_key=api_key)
    return _client


def generate_story(dog) -> str:
    """Generate a first-person AI personality story for a dog."""
    prompt = (
        f"You are writing a warm, first-person adoption profile story for a dog at a shelter. "
        f"Write 3-4 sentences in the dog's voice. Make it emotional, personal, and charming. "
        f"Do not mention the shelter name or specific locations.\n\n"
        f"Dog info:\n"
        f"- Name: {dog.name}\n"
        f"- Breed: {dog.breed}\n"
        f"- Age: {dog.raw_age} years old\n"
        f"- Gender: {dog.gender}\n"
        f"- Size: {dog.size}\n"
        f"- Tags: {', '.join(dog.tags) if dog.tags else 'none'}\n"
    )

    response = _get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.85,
    )
    return response.choices[0].message.content.strip()


def match_dogs(query: str, dogs: list) -> list:
    """
    Given a user lifestyle description and a list of dog dicts,
    return up to 3 recommended dog IDs with reasons.
    """
    dogs_summary = "\n".join(
        f"- ID {d['id']}: {d['name']}, {d['breed']}, {d['age']}, {d['gender']}, "
        f"size={d['size']}, city={d['city']}, tags={', '.join(d.get('tags', []))}"
        for d in dogs[:40]
    )

    prompt = (
        f"A user is looking to adopt a dog. Here is their lifestyle description:\n"
        f"\"{query}\"\n\n"
        f"Here are the available dogs:\n{dogs_summary}\n\n"
        f"Pick the top 3 best matches. Reply ONLY with a JSON array like:\n"
        f'[{{"id": 1, "reason": "Short reason why this dog fits"}}, ...]\n'
        f"Do not include any other text."
    )

    response = _get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.5,
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())
