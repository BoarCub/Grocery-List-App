from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    # Class attributes, could be inherited
    id = db.Column(db.Integer, primary_key=True, unique=True)  # primaryfro keys are required by SQLAlchemy
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)
    calories_daily = db.Column(db.Float, default=-1)
    guided = db.Column(db.Boolean, default=False)
    # dietary_type = db.Column(db.String(100), default=None)
    # nutrition = db.Column(db.)

    words = db.Column(db.String)
    bmi = db.Column(db.String)

    def __init__(self, email, name, password):
        self.email = email
        self.password = password
        self.name = name

    def is_active(self):
        """True, as all users are active."""
        return True

    # IF YOU ENCOUNTERED SOME ERRORS, READ THE DOCUMENT FIRST ! YOU MAY FIND THINGS USEFUL!
    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get_words(self):
        return self.words.split(',')

    def add_dietary(self, word):
        self.words += ',' + word

    def get_calories_daily(self):
        return self.calories_daily

    def get_rec(self):
        """Get recommended amount of every nutrient"""
        return {'cal': 0}

    def get_bmi(self):
        try:
            return int(self.bmi)
        except ValueError:
            return 0

    def is_guided(self):
        if not self.guided:
            self.guided = True
            return False
        return self.guided