"""
app/config.py (Configurations)
P.S. 但可有可無，不會影響評分 -zx

Purpose:
- A place where we store "app" settings.
- Keep __init__.py cleaner.
- Make future settings easier to manage.

TODO:
1. Add basic Config class
   - Create class Config.
   - Store common app settings inside it.

2. Add SECRET_KEY
   - Needed later for login and session.
   - Example:
     SECRET_KEY = "pickpet-dev-secret"

3. Add database path
   - Needed when the SQLite database is ready.
   - Example:
     DATABASE = "database/pickpet.db"
"""

# class Config:
#     SECRET_KEY = "pickpet-dev-secret"
#     DATABASE = "database/pickpet.db"