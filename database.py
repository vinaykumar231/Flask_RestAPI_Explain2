from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Function to initialize the database
def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/flask_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

# Function to get db session
def get_db():
    return db.session
