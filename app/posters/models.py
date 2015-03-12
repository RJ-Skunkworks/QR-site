from app.app_and_db import db
import re
from slugify import slugify
import time


class Poster(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(256), unique=True)
    # authors = db.Column(db.String(256), nullable=False)
    contact = db.Column(db.String(256), nullable=False, server_default='')
    date = db.Column(db.String(64), nullable=False, server_default='')
    abstract = db.Column(db.String(1024), nullable=False, server_default='')
    qr_image = db.Column(db.LargeBinary)

    def __setattr__(self, key, value):
        super(Poster, self).__setattr__(key, value)
        if key == 'slug' and value == '':
            self.slug = slugify(str(time.time()))
    
    # Relationships    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    authors = db.relationship('Author', backref='poster', lazy='dynamic')

    def __repr__(self):
        return '<Poster %r>' % self.title

class Author(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    social = db.Column(db.String(256), nullable=False, server_default='')
    poster_id = db.Column(db.Integer, db.ForeignKey('poster.id'))

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(64), nullable=False, server_default='')
    allowed_posters = db.Column(db.Integer)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float)

class Purchase(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String, nullable=False, server_default='')
    product = db.Column(db.Integer, db.ForeignKey('item.id')) 


# userpurchases = db.Table('userpurchases',
#     db.Column('purchase_id', db.Integer, db.ForeignKey('purchase.id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
# )

# Define the UserRoles association model
class UserPurchases(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    purchase_id = db.Column(db.Integer(), db.ForeignKey('purchase.id'))
