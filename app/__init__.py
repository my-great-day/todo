import os
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# создание экземпляра приложения
todo = Flask(__name__)
todo.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')
todo.config["JWT_SECRET_KEY"] = "super-secret"

jwt = JWTManager(todo)

# инициализирует расширения
db = SQLAlchemy(todo)

# регистрация blueprints
from .main import todo as main_blueprint
from .main import api

todo.register_blueprint(main_blueprint)
todo.register_blueprint(api, url_prefix='/api')

# import views

# from . import forum_views
# from . import admin_views
