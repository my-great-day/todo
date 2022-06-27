from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user

from app import api, db, jwt
from app.models import Users, Content


@api.route("/login", methods=["POST"])
def logins():
    username = request.json.get("username", None)
    password = request.json.get("username", None)

    user = Users.query.filter_by(email=username).one_or_none()
    key = Users.query.filter_by(key=password).one_or_none()
    if not user and not key:
        return jsonify("Wrong username or password"), 401

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


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.query.filter_by(id=identity).one_or_none()
