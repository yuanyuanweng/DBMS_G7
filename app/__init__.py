from flask import Flask
from app.database import close_db

def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = "database/pickpet.db"
    app.config["SECRET_KEY"] = "pickpet-secret-key-2025"
    app.teardown_appcontext(close_db)

    from app.main_routes import main
    from app.dogs.routes import dogs_bp
    from app.auth.routes import auth_bp
    from app.applications.routes import applications_bp
    from app.admin.routes import admin_bp
    from app.ai.routes import ai_bp

    app.register_blueprint(main)
    app.register_blueprint(dogs_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(ai_bp)

    return app
