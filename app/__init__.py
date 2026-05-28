from flask import Flask, url_for
from app.database import close_db

def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = "database/pickpet.db"
    
    # auth 功能加上密鑰
    app.config["SECRET_KEY"] = "shaoyu_pickpet_secret_key" 
    
    # 開啟除錯模式
    app.config["DEBUG"] = True 

    app.teardown_appcontext(close_db) 

    from app.main_routes import main
    from app.dogs.routes import dogs_bp
    from app.auth.routes import auth_bp    # 引入auth 藍圖
    from app.admin.routes import admin_bp  # 引入 admin 藍圖

    app.register_blueprint(main)
    app.register_blueprint(dogs_bp)
    app.register_blueprint(auth_bp)        # 註冊 auth 藍圖
    app.register_blueprint(admin_bp)      # 註冊 admin 藍圖

    @app.context_processor
    def inject_rescue_urls():
        def rescued_url_for(endpoint, **values):
            if endpoint == 'dogs.list':
                return url_for('dogs.list_dogs', **values)
            if endpoint == 'dogs.edit' and 'id' in values:
                dog_id = values.pop('id')
                return url_for('dogs.edit', dog_id=dog_id)
            return url_for(endpoint, **values)
        return dict(url_for=rescued_url_for)

    return app