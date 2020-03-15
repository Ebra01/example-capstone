import os
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

database_path = os.environ.get('CAPSTONE_DB')


def setup_db(app, db_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('CAPSTONE_SECRET')
    db.app = app
    db.init_app(app)
    db.create_all()


class Actors(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}"

    def display(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    availability = db.Column(db.DateTime)

    def __init__(self, title, release_data, availability):
        self.title = title
        self.release_date = release_data
        self.availability = availability

    def __repr__(self):
        return f"Title: {self.title}, Release Date: {self.release_date}, Availability: {self.availability}"

    def display(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'availability': self.availability
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
