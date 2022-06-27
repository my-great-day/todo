import os
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


todo = Flask(__name__)
todo.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')
todo.config["JWT_SECRET_KEY"] = "super-secret"

jwt = JWTManager(todo)

db = SQLAlchemy(todo)


from .main import todo as main_blueprint
from .main import api

todo.register_blueprint(main_blueprint)
todo.register_blueprint(api, url_prefix='/api')
