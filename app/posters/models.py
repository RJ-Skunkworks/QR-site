from app.app_and_db import db
import re
from slugify import slugify
import time


class Poster(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(256), unique=True)
    authors = db.Column(db.String(256), nullable=False)
    contact = db.Column(db.String(256), nullable=False, server_default='')
    date = db.Column(db.String(64), nullable=False, server_default='')
    abstract = db.Column(db.String(1024), nullable=False, server_default='')
    qr_image = db.Column(db.LargeBinary)

    # Relationships    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

    # def __setattr__(self, key, value):
    #     super(Poster, self).__setattr__(key, value)
    #     if key == 'title' :
    #         self.slug = slugify(self.title +"-"+self.id)

    def __repr__(self):
        return '<Poster %r>' % self.title

