'''
Temporary Dog model using mock data.

Current stage:
- Database schema is not finalized yet.
- Use mock data so frontend pages can be developed and tested.

TODO:
- Replace mock data with SQL queries after the database schema is finalized.
- Keep the method names the same if possible.
'''

MOCK_DOGS = [
    {
        'id': 1,
        'name': 'Komame',
        'breed': 'Shiba Inu Mix',
        'age': '2 yrs',
        'gender': 'Female',
        'city': 'Taipei',
        'is_urgent': True,
        'tags': ['Apartment-Friendly', 'Gentle'],
        'image_url': None,
        'ai_story': 'I love napping in sunny spots.',
        'color': '#D9A57A',
        'spot_color': '#C4714A'
    },
    {
        'id': 2,
        'name': 'Lucky',
        'breed': 'Mixed',
        'age': '4 yrs',
        'gender': 'Male',
        'city': 'Kaohsiung',
        'is_urgent': False,
        'tags': ['Friendly', 'Playful'],
        'image_url': None,
        'ai_story': 'I enjoy walks and meeting new friends.',
        'color': '#A98467',
        'spot_color': '#6F4E37'
    },
    {
        'id': 3,
        'name': 'Mochi',
        'breed': 'Taiwan Dog',
        'age': '1 yr',
        'gender': 'Female',
        'city': 'Tainan',
        'is_urgent': False,
        'tags': ['Smart', 'Energetic'],
        'image_url': None,
        'ai_story': 'I am curious, active, and ready for a loving home.',
        'color': '#B5C4B1',
        'spot_color': '#6B8C6B'
    },
    {
        'id': 4,
        'name': 'Bobo',
        'breed': 'Golden Retriever Mix',
        'age': '5 yrs',
        'gender': 'Male',
        'city': 'Taichung',
        'is_urgent': False,
        'tags': ['Gentle', 'Loyal'],
        'image_url': None,
        'ai_story': 'I am calm, loyal, and happiest beside my person.',
        'color': '#E8C4A0',
        'spot_color': '#C4A050'
    },
    {
        'id': 5,
        'name': 'Nana',
        'breed': 'Spitz Mix',
        'age': '3 yrs',
        'gender': 'Female',
        'city': 'New Taipei',
        'is_urgent': True,
        'tags': ['Small', 'Sweet'],
        'image_url': None,
        'ai_story': 'I may be small, but I have a big heart.',
        'color': '#D4A5A5',
        'spot_color': '#A07070'
    },
    {
        'id': 6,
        'name': 'Oreo',
        'breed': 'Mixed',
        'age': '7 yrs',
        'gender': 'Male',
        'city': 'Taipei',
        'is_urgent': False,
        'tags': ['Calm', 'Loyal'],
        'image_url': None,
        'ai_story': 'I enjoy quiet afternoons and would love a peaceful home.',
        'color': '#A8C5DA',
        'spot_color': '#5B8FA8'
    }
]

class Dog:
    '''
    Dog data provider.

    This class currently returns mock data.
    Later, these methods can be changed to use SQL.
    '''
    
    @staticmethod #Static method (Unrelated to class object)
    def get_featured(limit=6):
        '''
        Return a limited number of dogs for the homepage.
        '''
        return MOCK_DOGS[:limit]
    
    @staticmethod #Static method (Unrelated to class object)
    def get_all():
        '''
        Return all dogs for the dog listing page.
        '''
        return MOCK_DOGS

    @staticmethod
    def get_by_id(dog_id):
        '''
        Return one dog by ID.
        '''
        for dog in MOCK_DOGS:
            if dog['id'] == dog_id:
                return dog

        return None