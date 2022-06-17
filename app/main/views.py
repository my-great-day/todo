from flask import render_template, request, redirect, url_for, session, jsonify
from flask_jwt_extended import create_access_token, current_user, jwt_required

from app import db, todo, jwt
from app.models import Content, Users


@todo.route('/')
def index():
    return render_template('index.html')


@todo.route('/add_todo/<id>', methods=['post', 'get'])
def add_todo(id):
    print(id, '\n', session.get('todo'))
    msg = ''
    if id == session.get('todo'):
        if request.form.get('add_text') is not None and request.form.get('add_text') != '':
            content = Content(text=request.form.get('add_text'), check_slug=id.lower())
            db.session.add(content)
            db.session.commit()
            msg = 'Текст добавлено!'
            return redirect(url_for('.add_todo', id=id))
        incomplete_list = Content.query.filter_by(check_mark=False, check_slug=id.lower()).all()
        complete_list = Content.query.filter_by(check_mark=True, check_slug=id.lower()).all()
    else:
        return redirect(url_for('.login'))
    return render_template('add_todo.html', msg=msg, incomplete_list=incomplete_list,
                           complete_list=complete_list, users=id)


def log_test(email, password):
    data = db.session.query(Users.email, Users.key).filter_by(email=email, key=password).all()
    try:
        if email == data[0][0] and password == data[0][1]:
            msg = 'OK'
        else:
            msg = 'Не правилный логин или пороль!!'
    except IndexError:
        msg = 'Не правилный логин или пороль!!'
    return msg


@todo.route('/register/', methods=["post", "get"])
def register():
    if session.get('todo'):
        session.pop('todo')
    reg = request.form.get('email')
    if reg is not None and reg != '':
        email = request.form.get('email')
        msg = log_test(email=email, password=request.form.get('password'))
        if msg == 'OK':
            session['todo'] = email
            return redirect(url_for('.add_todo', id=email))

        else:
            content = Users(name=request.form.get('name'), slug=reg.lower(), email=reg,
                            key=request.form.get('password'))
            db.session.add(content)
            db.session.commit()
            session['todo'] = reg
            return redirect(url_for('.add_todo', id=reg))
    return render_template('register.html')


@todo.route('/login/', methods=["post", "get"])
def login():
    if session.get('todo'):
        session.pop('todo')
    msg = ''
    if request.method == 'POST':
        email = request.form.get('email')
        msg = log_test(email=email, password=request.form.get('password'))
        if msg == 'OK':
            session['todo'] = email
            return redirect(url_for('.add_todo', id=email))
    return render_template('login.html', msg=msg)


@todo.route('/complete/<user>/<id>')
def complete(user, id):
    comp = Content.query.filter_by(id=int(id)).first()
    comp.check_mark = True
    db.session.commit()
    return redirect(url_for('.add_todo', id=user))


@todo.route('/delete/<user>/<id>')
def delete(user, id):
    comp = Content.query.filter_by(id=int(id)).first()
    db.session.delete(comp)
    db.session.commit()
    return redirect(url_for('.add_todo', id=user))


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.query.filter_by(id=identity).one_or_none()
