'''
This file creates the Flask application and registers all Blueprints.
统一创建 Flask 应用并注册所有蓝图。

TODO: 
- Import objects 
- Register Blueprints like 'main, auth, dogs, applications, admin'
'''

from flask import Flask, render_template
from .main_routes import main 

def create_app():
    '''Register all Blueprints and return the app instance.'''
    app = Flask(__name__)
    app.register_blueprint(main)
    
    return app 