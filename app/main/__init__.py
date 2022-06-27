from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, current_user, jwt_required

from .. import db

todo = Blueprint('todo', __name__, template_folder='templates', static_folder='static')
api = Blueprint('api', __name__)

from . import views
from ..models import Users, Content
