from tickets import db, login_manager
from tickets import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Float(), nullable=False, default=1000)
    is_admin = db.Column(db.Boolean(), nullable=False, default='false')

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text):
        self.password_hash = bcrypt.generate_password_hash(password=plain_text).decode('utf-8')

    def check_password(self, attempted_user):
        return bcrypt.check_password_hash(self.password_hash, attempted_user)


class Venue(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    venue_name = db.Column(db.String(length=30), nullable=False, unique=True)
    venue_address = db.Column(db.String(length=50), nullable=False)


class Show(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    show_name = db.Column(db.String(length=30), nullable=False)
    show_timings = db.Column(db.String(length=50), nullable=False)
    rating = db.Column(db.Float(), nullable=False)
    ticket_rate = db.Column(db.Float(), nullable=False)
    at_venue = db.Column(db.Integer(), nullable=False)
    no_of_seats = db.Column(db.Integer(), nullable=False)
    img_url = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    lang = db.Column(db.String(), nullable=False)


class Tickets(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    show_id = db.Column(db.Integer(), nullable=False)
    no_of_tickets = db.Column(db.Integer(), nullable=False)
    username = db.Column(db.String(length=30), nullable=False)


class Reviews(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    show_id = db.Column(db.Integer(), nullable=False)
    # review = db.Column(db.String(length=100))
    rating = db.Column(db.Float(), nullable=False)
    username = db.Column(db.String(length=30), nullable=False)


class Genre(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    show_id = db.Column(db.Integer(), nullable=False)
    genre = db.Column(db.String(), nullable=False)
    venue_id = db.Column(db.Integer(), nullable=False)

#
# class New(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     show_id = db.Column(db.Integer(), nullable=False)
#     genre = db.Column(db.String(), nullable=False)
#     venue_id = db.Column(db.Integer(), nullable=False)
