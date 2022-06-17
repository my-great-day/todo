from datetime import datetime

from app.main.views import db


class Content(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.Integer(), primary_key=True)
    check_slug = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    check_mark = db.Column(db.Boolean(), default=False)
    create_on = db.Column(db.DateTime(), default=datetime.now().isoformat(timespec='seconds'))


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=False)
    slug = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=False)
    key = db.Column(db.String(100), nullable=False, unique=False)
