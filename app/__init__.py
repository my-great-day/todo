import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# создание экземпляра приложения
todo = Flask(__name__)
todo.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

# инициализирует расширения
db = SQLAlchemy(todo)

# import views
from . import views
# from . import forum_views
# from . import admin_views
