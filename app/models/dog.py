COLORS = ['#D9A57A', '#B5C4B1', '#A8C5DA', '#D4A5A5', '#C4B5A5', '#E8C4A0', '#9DB5A0', '#C4A8C4']
SPOT_COLORS = ['#C4714A', '#6B8C6B', '#5B8FA8', '#A07070', '#8B7355', '#C4A050', '#5B7A6B', '#9A7A9A']


class Dog:
    def __init__(self, row):
        self.id = row['Dog_ID']
        self.name = (row['Name'] or '').strip() or 'Unknown'
        self.breed = row['Breed'] or 'Mixed Breed'
        age = row['Age'] or 0
        self.age = f"{max(1, int(age * 12))} mo" if age < 1 else f"{int(age)} yrs"
        self.gender = (row['Gender'] or 'unknown').capitalize()
        self.city = row.get('City') or 'Taipei'
        self.size = row.get('Size') or self._derive_size()
        self.image_url = row['Image_URL']
        self.is_urgent = bool(row.get('Is_Urgent', 0))
        idx = self.id % len(COLORS)
        self.color = COLORS[idx]
        self.spot_color = SPOT_COLORS[idx]
        self.tags = self._derive_tags(row)
        self.ai_story = row['AI_Story']
        self.description = row['AI_Story']
        self.health_status = None
        self.shelter = None

    def _derive_size(self):
        breed = self.breed.lower()
        if any(x in breed for x in ['dachshund', 'spitz', 'schnauzer', 'chihuahua']):
            return 'Small'
        if any(x in breed for x in ['golden', 'labrador', 'rottweiler', 'husky', 'boxer',
                                      'tibetan', 'bernese', 'staffordshire', 'german pointer',
                                      'rhodesian']):
            return 'Large'
        return 'Medium'

    def _derive_tags(self, row):
        age = row['Age'] or 0
        tags = []
        if age < 2:
            tags.append('🐶 Puppy')
        if age > 10:
            tags.append('🧡 Senior')
        tags.append(f'📏 {self._derive_size()}')
        tags.append('♀ Female' if self.gender == 'Female' else '♂ Male')
        return tags[:3]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'breed': self.breed,
            'age': self.age,
            'gender': self.gender,
            'city': self.city,
            'size': self.size,
            'image_url': self.image_url,
            'is_urgent': self.is_urgent,
            'color': self.color,
            'spot_color': self.spot_color,
            'tags': self.tags,
            'ai_story': self.ai_story,
        }
