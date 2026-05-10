from flask import Flask

def create_app():
    """
    Create Flask app and register blueprints.

    TODO:
    - Add database config (After finished building database)
    - Add secret key (After finished building auth)
    """

    app = Flask(__name__)

    from app.main_routes import main
    from app.dogs.routes import dogs_bp

    app.register_blueprint(main)
    app.register_blueprint(dogs_bp)

    return app