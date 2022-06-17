from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, current_user, jwt_required

todo = Blueprint('todo', __name__, template_folder='templates', static_folder='static')
api = Blueprint('api', __name__)

from . import views
from ..models import Users


@api.route("/login", methods=["POST"])
def logins():
    username = request.json.get("username", None)
    password = request.json.get("username", None)

    user = Users.query.filter_by(name=username).one_or_none()
    key = Users.query.filter_by(key=password).one_or_none()
    if not user and not key:
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@api.route("/get_res", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        password=current_user.key,
    )
