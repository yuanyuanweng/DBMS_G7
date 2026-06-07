from app.database import get_db
from app.models.shelter import Shelter

COLORS = [
    "#D9A57A", "#B5C4B1", "#A8C5DA", "#D4A5A5",
    "#C4B5A5", "#E8C4A0", "#9DB5A0", "#C4A8C4",
]

SPOT_COLORS = [
    "#C4714A", "#6B8C6B", "#5B8FA8", "#A07070",
    "#8B7355", "#C4A050", "#5B7A6B", "#9A7A9A",
]

SMALL_BREEDS = ("chihuahua", "dachshund", "terrier", "spitz")
LARGE_BREEDS = (
    "boxer", "retriever", "ridgeback", "bernese", "husky",
    "rottweiler", "german pointer", "labrador",
)


class Dog:
    """Dog data object backed by the SQLite database."""

    def __init__(self, row):
        """Convert one database row into a frontend-friendly Dog object."""
        data = dict(row)

        self.id = data["Dog_ID"]
        self.shelter_id = data["Shelter_ID"]
        self.name = data["Name"]
        self.breed = data.get("Breed") or "Unknown Mix"
        self.raw_age = int(data.get("Age") or 0)
        self.age = f"{self.raw_age} yrs"
        self.gender = data.get("Gender") or "Unknown"
        self.image_url = data.get("Image_URL")
        self.availability = data.get("Availability") or "Available"

        self.shelter = Shelter.get_by_id(self.shelter_id)
        self.city = self._derive_city()
        self.size = self._derive_size()
        self.health_status = self._latest_health_status()
        self.description = self._derive_description()
        self.ai_story = ""
        self.is_urgent = False

        self.color = COLORS[(self.id - 1) % len(COLORS)]
        self.spot_color = SPOT_COLORS[(self.id - 1) % len(SPOT_COLORS)]
        self.tags = self._derive_tags()

    def _derive_city(self):
        """Infer city from shelter name/location until City is added to Dog."""
        source = ""
        if self.shelter:
            source = f"{self.shelter.name} {self.shelter.location}".lower()

        if "taipei" in source:
            return "Taipei"
        if "new taipei" in source:
            return "New Taipei"
        if "taichung" in source:
            return "Taichung"
        if "tainan" in source:
            return "Tainan"
        if "kaohsiung" in source:
            return "Kaohsiung"
        return "Unknown"

    def _derive_size(self):
        """Estimate dog size from breed until Size is added to Dog."""
        breed = self.breed.lower()
        if any(keyword in breed for keyword in SMALL_BREEDS):
            return "Small"
        if any(keyword in breed for keyword in LARGE_BREEDS):
            return "Large"
        return "Medium"

    def _derive_tags(self):
        """Generate display tags for dog cards and detail pages."""
        tags = [self.size, self.gender]

        if self.raw_age < 1:
            tags.append("Puppy")
        elif self.raw_age >= 8:
            tags.append("Senior")

        if self.availability != "Available":
            tags.append(self.availability)

        return tags

    def _derive_description(self):
        """Create a short fallback description from known database fields."""
        shelter_name = self.shelter.name if self.shelter else "the shelter"
        return (
            f"{self.name} is a {self.age} {self.breed} currently cared for by "
            f"{shelter_name}. Contact the shelter for more details."
        )

    def _latest_health_status(self):
        """Return the latest recorded vaccine name for this dog, if present."""
        db = get_db()
        row = db.execute(
            """
            SELECT Vaccine_Name
            FROM Health_record
            WHERE Dog_ID = ?
            ORDER BY Administered_Date DESC, Record_ID DESC
            LIMIT 1
            """,
            (self.id,),
        ).fetchone()
        return row["Vaccine_Name"] if row else None

    def to_dict(self):
        """Convert Dog object to dictionary for JSON usage."""
        return {
            "id": self.id,
            "shelter_id": self.shelter_id,
            "name": self.name,
            "breed": self.breed,
            "age": self.age,
            "raw_age": self.raw_age,
            "gender": self.gender,
            "city": self.city,
            "size": self.size,
            "image_url": self.image_url,
            "availability": self.availability,
            "ai_story": self.ai_story,
            "description": self.description,
            "health_status": self.health_status,
            "is_urgent": self.is_urgent,
            "color": self.color,
            "spot_color": self.spot_color,
            "tags": self.tags,
        }

    @staticmethod
    def _base_query():
        return """
            SELECT Dog_ID, Shelter_ID, Name, Gender, Age, Breed, Image_URL, Availability
            FROM Dog_With_Status
        """

    @staticmethod
    def get_featured(limit=4):
        """Return a limited number of dogs for the homepage."""
        db = get_db()
        rows = db.execute(
            f"""
            {Dog._base_query()}
            ORDER BY Dog_ID DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [Dog(row) for row in rows]

    @staticmethod
    def get_all():
        """Return all non-adopted dogs for the dog listing page."""
        db = get_db()
        rows = db.execute(
            f"""
            {Dog._base_query()}
            WHERE Availability != 'Adopted'
            ORDER BY Dog_ID DESC
            """
        ).fetchall()
        return [Dog(row) for row in rows]

    @staticmethod
    def get_by_id(dog_id):
        """Return one dog by ID."""
        db = get_db()
        row = db.execute(
            f"""
            {Dog._base_query()}
            WHERE Dog_ID = ?
            """,
            (dog_id,),
        ).fetchone()
        return Dog(row) if row else None

    @staticmethod
    def create(shelter_id, name, gender, age, breed, image_url=None):
        """Create a dog record and return the new dog ID."""
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO Dog (Shelter_ID, Name, Gender, Age, Breed, Image_URL)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (shelter_id, name, gender, age, breed, image_url),
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update(dog_id, shelter_id, name, gender, age, breed, image_url=None):
        """Update one dog record and return whether a row was changed."""
        db = get_db()
        cursor = db.execute(
            """
            UPDATE Dog
            SET Shelter_ID = ?, Name = ?, Gender = ?, Age = ?, Breed = ?, Image_URL = ?
            WHERE Dog_ID = ?
            """,
            (shelter_id, name, gender, age, breed, image_url, dog_id),
        )
        db.commit()
        return cursor.rowcount > 0

    @staticmethod
    def search(q="", gender="", age_group="", size="", city="", sort="newest"):
        """Search dogs with URL filter parameters."""
        dogs = Dog.get_all()

        if q:
            query = q.lower()
            dogs = [
                dog for dog in dogs
                if query in dog.name.lower() or query in dog.breed.lower()
            ]

        if gender:
            dogs = [dog for dog in dogs if dog.gender == gender]

        if age_group:
            if age_group == "puppy":
                dogs = [dog for dog in dogs if dog.raw_age < 1]
            elif age_group == "young":
                dogs = [dog for dog in dogs if 1 <= dog.raw_age < 3]
            elif age_group == "adult":
                dogs = [dog for dog in dogs if 3 <= dog.raw_age < 8]
            elif age_group == "senior":
                dogs = [dog for dog in dogs if dog.raw_age >= 8]

        if size:
            dogs = [dog for dog in dogs if dog.size == size]

        if city:
            dogs = [dog for dog in dogs if dog.city == city]

        if sort == "oldest":
            dogs = sorted(dogs, key=lambda dog: dog.id)
        elif sort == "age_asc":
            dogs = sorted(dogs, key=lambda dog: dog.raw_age)
        elif sort == "age_desc":
            dogs = sorted(dogs, key=lambda dog: dog.raw_age, reverse=True)
        else:
            dogs = sorted(dogs, key=lambda dog: dog.id, reverse=True)

        return dogs
