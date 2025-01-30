# **Flask Property API with MySQL**

This is a simple REST API built using **Flask**, **SQLAlchemy**, and **MySQL**. The API allows you to interact with property-related data, including creating and retrieving property details. It uses **MySQL** as the database and **SQLAlchemy** for ORM-based data management.

## **Prerequisites**

Before running the application, make sure you have the following installed:

- **Python 3.12.2**
- **MySQL Server**
- **pip** or **pipenv** for managing Python packages

## **Installation**

### **1. Clone the repository:**

```bash
git clone https://github.com/vinaykumar231/Flask_RestAPI_Explain.git
cd flask-property-api

 Install dependencies:
pip install -r requirements.txt

change .env and setting file for database connection

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


run this command
python app.py --reload
