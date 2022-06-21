from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, current_user, jwt_required

from .. import db

todo = Blueprint('todo', __name__, template_folder='templates', static_folder='static')
api = Blueprint('api', __name__)

from . import views
from ..models import Users, Content


@api.route("/login", methods=["POST"])
def logins():
    email = request.json.get("email", None)
    password = request.json.get("username", None)

    user = Users.query.filter_by(email=email).one_or_none()
    key = Users.query.filter_by(key=password).one_or_none()
    if not user and not key:
        return jsonify("Wrong email or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@api.route("/get_res", methods=["GET"])
@jwt_required()
def protected():
    result, result1 = [], []
    complete_list = db.session.query(Content.text).filter_by(check_slug=current_user.email, check_mark=True).all()
    for t in complete_list: result.append(t[0])

    incomplete_list = db.session.query(Content.text).filter_by(check_slug=current_user.email, check_mark=False).all()
    for t in incomplete_list: result1.append(t[0])

    return jsonify(
        username=current_user.name,
        complete_list=result,
        incomplete_list=result1,
    )
