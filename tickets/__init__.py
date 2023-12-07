from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SECRET_KEY'] = "c21b1ee4f73b652fac67258d"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # for storing passwords securely
login_manager = LoginManager(app)  # provides session management for users
login_manager.login_view = 'login_page'  # for going to the login page when logged out

login_manager.login_message_category = "info"

from tickets import routes

with app.app_context():
    db.create_all()
