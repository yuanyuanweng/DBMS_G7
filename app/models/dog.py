'''
- Data Source (main_routes.py, dogs/routes.py depends on this file)
- Provides Dog object with class attributes & methods for consistency

TODO:
- Replace mock data with SQL queries after the database schema is finalized.
'''
COLORS = [
    '#D9A57A', '#B5C4B1', '#A8C5DA', '#D4A5A5',
    '#C4B5A5', '#E8C4A0', '#9DB5A0', '#C4A8C4'
]

SPOT_COLORS = [
    '#C4714A', '#6B8C6B', '#5B8FA8', '#A07070',
    '#8B7355', '#C4A050', '#5B7A6B', '#9A7A9A'
]

MOCK_DOGS = [
    {
        'Dog_ID': 1,
        'Shelter_ID': 1,
        'Name': 'Komame',
        'Breed': 'Shiba Inu Mix',
        'Age': 2,
        'Gender': 'Female',
        'City': 'Taipei',
        'Size': 'Small',
        'Image_URL': None,
        'Availability': 'Available',
        'Is_Urgent': 0,
        'Is_Liked': 0,
        'AI_Story': 'I love napping in sunny spots and taking slow walks with gentle people.',
        'Tags': ['🏷 Small', '♀ Female']
    },
    {
        'Dog_ID': 2,
        'Shelter_ID': 1,
        'Name': 'Kendy',
        'Breed': 'Unknown Mix',
        'Age': 7,
        'Gender': 'Male',
        'City': 'Taipei',
        'Size': 'Medium',
        'Image_URL': None,
        'Availability': 'Available',
        'Is_Urgent': 0,
        'Is_Liked': 1,
        'AI_Story': 'No story yet — click to generate one with AI!',
        'Tags': ['🏷 Medium', '♂ Male']
    },
    {
        'Dog_ID': 3,
        'Shelter_ID': 2,
        'Name': 'Mochi',
        'Breed': 'Golden Retriever Mix',
        'Age': 4,
        'Gender': 'Female',
        'City': 'New Taipei',
        'Size': 'Large',
        'Image_URL': None,
        'Availability': 'Pending',
        'Is_Urgent': 1,
        'Is_Liked': 0,
        'AI_Story': 'I am friendly, energetic, and always ready for a walk or a game.',
        'Tags': ['🏷 Large', '♀ Female']
    },
    {
        'Dog_ID': 4,
        'Shelter_ID': 2,
        'Name': 'Bobo',
        'Breed': 'Taiwan Dog Mix',
        'Age': 1,
        'Gender': 'Male',
        'City': 'Taichung',
        'Size': 'Medium',
        'Image_URL': None,
        'Availability': 'Available',
        'Is_Urgent': 0,
        'Is_Liked': 0,
        'AI_Story': 'I am still young and curious. I hope to grow up with a family who loves adventure.',
        'Tags': ['🐶 Puppy', '♂ Male']
    },
    {
        'Dog_ID': 5,
        'Shelter_ID': 3,
        'Name': 'Luna',
        'Breed': 'Labrador Mix',
        'Age': 5,
        'Gender': 'Female',
        'City': 'Tainan',
        'Size': 'Large',
        'Image_URL': None,
        'Availability': 'Available',
        'Is_Urgent': 0,
        'Is_Liked': 1,
        'AI_Story': 'I am calm, loyal, and happiest when I can stay close to someone I trust.',
        'Tags': ['🏷 Large', '♀ Female']
    },
    {
        'Dog_ID': 6,
        'Shelter_ID': 3,
        'Name': 'Lucky',
        'Breed': 'Chihuahua Mix',
        'Age': 10,
        'Gender': 'Male',
        'City': 'Kaohsiung',
        'Size': 'Small',
        'Image_URL': None,
        'Availability': 'Adopted',
        'Is_Urgent': 0,
        'Is_Liked': 0,
        'AI_Story': 'I may be small, but I have a brave heart and lots of love to give.',
        'Tags': ['🏷 Small', '♂ Male']
    },
    {
        'Dog_ID': 7,
        'Shelter_ID': 4,
        'Name': 'Nana',
        'Breed': 'Mixed Breed',
        'Age': 11,
        'Gender': 'Female',
        'City': 'Taipei',
        'Size': 'Medium',
        'Image_URL': None,
        'Availability': 'Available',
        'Is_Urgent': 0,
        'Is_Liked': 0,
        'AI_Story': 'I am a gentle senior dog who enjoys quiet days, soft blankets, and kind voices.',
        'Tags': ['🧡 Senior', '♀ Female']
    },
    {
        'Dog_ID': 8,
        'Shelter_ID': 4,
        'Name': 'Rocky',
        'Breed': 'Husky Mix',
        'Age': 3,
        'Gender': 'Male',
        'City': 'New Taipei',
        'Size': 'Large',
        'Image_URL': None,
        'Availability': 'Pending',
        'Is_Urgent': 1,
        'Is_Liked': 1,
        'AI_Story': 'I have lots of energy and would love a home that enjoys outdoor activities.',
        'Tags': ['🏷 Large', '♂ Male']
    }
]

class Dog:
    '''
    Dog data object and data provider 
    '''
    
    # Constructor
    def __init__(self, row):
        '''
        Convert one raw dog row into a frontend-friendly Dog object
        '''
        self.id = row['Dog_ID']
        self.name = row['Name']
        self.breed = row.get('Breed') or 'Unknown Mix'
        self.age = f"{row['Age']} yrs"
        self.gender = row.get('Gender') or 'Unknown'
        self.city = row.get('City') or 'Unknown'
        self.size = row.get('Size') or 'Medium'
        self.image_url = row.get('Image_URL')
        self.ai_story = row.get('AI_Story') or 'No story yet — click to generate one with AI!'
        self.is_urgent = bool(row.get('Is_Urgent', 0))
        self.availability = row.get('Availability') or 'Available'
        self.color = COLORS[(self.id - 1) % len(COLORS)]
        self.spot_color = SPOT_COLORS[(self.id - 1) % len(SPOT_COLORS)]
        self.tags = row.get('Tags') or [f'🏷 {self.size}', f'{"♂" if self.gender == "Male" else "♀"} {self.gender}']
        
    
    # Helper method in 'Dog' class (Not meant to be called directly from outside)
    # mostly Used in constructor, but still it's a convention with normal behavior
    def _derive_size(self):
        '''
        TODO
        Estimate dog size based on breed if Size is not provided 
        '''
    
    # Helper method in 'Dog' class (Not meant to be called directly from outside)
    # mostly Used in constructor, but still it's a convention with normal behavior
    def _derive_tags(self, row):
        '''
        TODO
        Generate display tags for dog cards
        '''
        
    def to_dict(self):
        '''
        Convert Dog object to dictionary 
        Purpose: Dictionary (Python reference data type) -> JSON(Text/Data)
        '''
        return {
        'id': self.id,
        'name': self.name,
        'breed': self.breed,
        'age': self.age,
        'gender': self.gender,
        'city': self.city,
        'size': self.size,
        'image_url': self.image_url,
        'ai_story': self.ai_story,
        'is_urgent': self.is_urgent,
        'color': self.color,
        'tags': self.tags,
    }
    
    
    @staticmethod # Cannot directly access or modify object data = no self
    def get_featured(limit=4):
        '''
        Return a limited number of dogs for the homepage.
        '''
        return [Dog(row) for row in MOCK_DOGS[:limit]]
        
    
    @staticmethod # Cannot directly access or modify object data = no self
    def get_all():
        '''
        Return all dogs for the dog listing page.
        '''
        return [Dog(row) for row in MOCK_DOGS]
        

    @staticmethod
    def get_by_id(dog_id):
        '''
        Return one dog by ID.
        '''
        for row in MOCK_DOGS:
            if row['Dog_ID'] == dog_id:
                return Dog(row)
            
        return None
    
    # Used in dogs/list.html
    @staticmethod
    def search(q='', city='', size='', page=1, per_page=16):
        '''
        Search and paginate dogs 
        '''
        
        