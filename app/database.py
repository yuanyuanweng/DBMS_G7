import sqlite3
from flask import current_app, g 

def get_db():
    '''
    Database connection
    '''
    
    # Check this do we have a database connection already? (In current Req)
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row # We can access columns by name
        
    return g.db

def close_db(e=None):
    '''
    Closes database connection
    '''
    db = g.pop("db", None)
    
    if db is not None:
        db.close()