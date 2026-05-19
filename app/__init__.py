from flask import Flask
from app.database import close_db

def create_app():
    """
    Create Flask app and register blueprints.

    TODO:
    - Add secret key (After finished building auth)
    """

    app = Flask(__name__)
    app.config["DATABASE"] = "database/pickpet.db"
    app.teardown_appcontext(close_db) # automatically closes after each req ends

    from app.main_routes import main
    from app.dogs.routes import dogs_bp

    app.register_blueprint(main)
    app.register_blueprint(dogs_bp)

    return app