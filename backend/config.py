from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Inizializzazione Flask e SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apartment_booking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("Database Path:", os.path.abspath('apartment_booking.db'))
    return app
