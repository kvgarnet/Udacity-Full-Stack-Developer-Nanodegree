# ----------------------------------------------------------------------------#
# Contains all Database configuration, models and relationships.
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request, Response, flash, redirect, url_for,abort,jsonify
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, sqlalchemy

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db, compare_type=True)
# TODO: connect to a local postgresql database
#  kv: added config in config.py,verify with below
# print(f"my sqlalchemy dburl is {app.config['SQLALCHEMY_DATABASE_URI']}" )

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# Based on lesson 18,Implement Venue and Artist models relationship with 'Show' Table
Show = db.Table('Show',
                db.Column('id', db.Integer, primary_key=True),
                db.Column('Venue_id', db.Integer, db.ForeignKey('Venue.id'), nullable=False),
                db.Column('Artist_id', db.Integer, db.ForeignKey('Artist.id'), nullable=False),
                db.Column('start_time', db.DateTime, nullable=False)
                )


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String(120)))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))

    artists = db.relationship('Artist', secondary=Show, backref=db.backref('venues'), lazy=True)

    def __repr__(self):
        return f'<My Venue {self.id}: {self.name}>'


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String(130)))
    website = db.Column(db.String(200))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

    def __repr__(self):
        return f'<My Artist {self.id}: {self.name}>'
