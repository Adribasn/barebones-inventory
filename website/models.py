from . import db
from flask_login import UserMixin

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(8192))
    units = db.Column(db.Integer)
    price = db.Column(db.Float)
    value = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    firstName = db.Column(db.String(256))
    password = db.Column(db.String(256))
    items = db.relationship('Item')