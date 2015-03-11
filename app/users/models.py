from flask_user import UserMixin
from app.app_and_db import db


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User email information (required for Flask-User)
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(50), nullable=False, server_default='')
    last_name = db.Column(db.String(50), nullable=False, server_default='')

    # Relationships
    user_auth = db.relationship('UserAuth', uselist=False)
    posters = db.relationship('Poster', backref='poster', lazy='dynamic')

    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    purchases = db.relationship('Purchase', secondary='user_purchases', backref=db.backref('users', lazy='dynamic'))
    remaining_posters = db.Column(db.Integer, server_default='1')


# Define the UserAuth data model.
class UserAuth(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))

    # User authentication information (required for Flask-User)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # Relationships
    user = db.relationship('User', uselist=False)


# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))


# Define the UserRoles association model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

