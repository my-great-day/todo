from flask import Blueprint

todo = Blueprint('todo', __name__, template_folder='templates', static_folder='static')

from . import views
