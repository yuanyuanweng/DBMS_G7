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
        self.raw_age = int(row['Age'])
        self.age = f"{self.raw_age} yrs"
        self.gender = row.get('Gender') or 'Unknown'
        self.city = row.get('City') or 'Unknown'
        self.size = row.get('Size') or 'Medium'
        self.image_url = row.get('Image_URL')
        self.ai_story = row.get('AI_Story') or 'No story yet — click to generate one with AI!'
        self.is_urgent = bool(row.get('Is_Urgent', 0))
        self.is_liked = bool(row.get('Is_Liked', 0))
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
        'is_liked': self.is_liked,
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
        

    @staticmethod # Cannot directly access or modify object data = no self
    def get_by_id(dog_id):
        '''
        Return one dog by ID.
        '''
        for row in MOCK_DOGS:
            if row['Dog_ID'] == dog_id:
                return Dog(row)
            
        return None
    
    @staticmethod # Cannot directly access or modify object data = no self
    def search(q="", gender="", age_group="", size="", city="", sort="newest"):
        '''
        Used in dogs/list.html
        Search dogs with URL parameters
        '''
        dogs = [Dog(row) for row in MOCK_DOGS]
        
        # 根據用戶輸入的搜尋欄
        if q:
            q = q.lower()
            dogs = [
                dog for dog in dogs
                if q in dog.name.lower()
                or q in dog.breed.lower()
            ]
        
        # 根據性別
        if gender: 
            dogs = [dog for dog in dogs if dog.gender == gender]
        
        # 根據4種年齡區間
        if age_group:
            if age_group == "puppy":
                dogs = [dog for dog in dogs if dog.raw_age < 1]
            elif age_group == "young":
                dogs = [dog for dog in dogs if 1 <= dog.raw_age < 3]
            elif age_group == "adult":
                dogs = [dog for dog in dogs if 3 <= dog.raw_age < 8]
            elif age_group == "senior":
                dogs = [dog for dog in dogs if dog.raw_age >= 8]
        
        # 根據體型
        if size:
            dogs = [dog for dog in dogs if dog.size == size]
        
        # 根據城市
        if city:
            dogs = [dog for dog in dogs if dog.city == city]
        
        # 支持 狗狗新增時間 & 年齡大小
        if sort == "newest": 
            dogs = sorted(dogs, key=lambda dog: dog.id, reverse=True)
        elif sort == "oldest":
            dogs = sorted(dogs, key=lambda dog: dog.id)
        elif sort == "age_asc":
            dogs = sorted(dogs, key=lambda dog: dog.raw_age)
        elif sort == "age_desc":
            dogs = sorted(dogs, key=lambda dog: dog.raw_age, reverse=True)
            
        return dogs