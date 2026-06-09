from flask import Flask, session
from app.database import close_db
from app.db_migrations import run_startup_migrations


def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = "database/pickpet.db"
    app.config["SECRET_KEY"] = "pickpet-secret-key-2025"
    app.teardown_appcontext(close_db)
    
    run_startup_migrations(app)

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

    @app.context_processor
    def inject_notif_count():
        user_id = session.get('user_id')
        if not user_id:
            return {'notif_count': 0}
        try:
            from app.models.application import Application
            count = Application.count_unseen_updates(user_id)
        except Exception:
            count = 0
        return {'notif_count': count}

    return app
