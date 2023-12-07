from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from tickets.models import User


class registerForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists!')

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email_address=email_to_check.data).first()
        if user:
            raise ValidationError('Email already Exists')

    username = StringField(label="Username: ", validators=[Length(min=3, max=30), DataRequired()])
    email = EmailField(label="Email: ", validators=[Length(max=40), DataRequired(), Email()])
    password1 = PasswordField(label="Password: ", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(label="Confirm Password: ", validators=[DataRequired(), EqualTo('password1')])
    isAdmin = BooleanField(label="Admin?")
    submit = SubmitField(label="Create a Account")


class LoginForm(FlaskForm):
    username = StringField(label="Username: ", validators=[DataRequired()])
    password = PasswordField(label="Password: ", validators=[DataRequired()])
    submit = SubmitField(label="Login")


class addVenue(FlaskForm):
    username = StringField(label="Venue Name: ", validators=[DataRequired()])
    venueaddress = StringField(label="Venue Address: ", validators=[DataRequired()])
    submit = SubmitField(label="Add Venue")


class addShow(FlaskForm):
    show_name = StringField(label="Show Name: ", validators=[DataRequired()])
    show_timings = StringField(label="Show Timings: ", validators=[DataRequired()])
    rating = StringField(label="IMDB Rating", validators=[DataRequired()])
    ticket_rate = StringField(label="Ticket Rate", validators=[DataRequired()])
    no_of_seats = StringField(label="No of Seats", validators=[DataRequired()])
    img_url = StringField(label="Image URL: ", validators=[DataRequired()])
    category = StringField(label="2D/3D/IMAX: ", validators=[DataRequired()])
    lang = StringField(label="Language: ", validators=[DataRequired()])
    submit = SubmitField(label="Add Show")


class BookTickets(FlaskForm):
    tickets = StringField(label="No of Tickets: ", validators=[DataRequired()])
    phone_no = StringField(label="Phone Number: ", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField(label="Confirm Booking")


class Search(FlaskForm):
    search = StringField(label="Search", validators=[DataRequired()])
    submit = SubmitField(label="Search")


class ReviewForm(FlaskForm):
    review = TextAreaField(label="Movie reviews", validators=[DataRequired()])
    rating = StringField(label="Rate the Movie", validators=[DataRequired()])
    submit = SubmitField(label="Submit Review")


class GenreForm(FlaskForm):
    action = BooleanField(label="Action: ")
    adventure = BooleanField(label="Adventure: ")
    comedy = BooleanField(label="Comedy: ")
    drama = BooleanField(label="Drama: ")
    fantasy = BooleanField(label="Fantasy: ")
    horror = BooleanField(label="Horror: ")
    musical = BooleanField(label="Musical: ")
    mystery = BooleanField(label="Mystery: ")
    romance = BooleanField(label="Romance: ")
    scifi = BooleanField(label="Sci-Fi: ")
    thriller = BooleanField(label="Thriller: ")
    sports = BooleanField(label="Sports: ")
    western = BooleanField(label="Western: ")
    crime = BooleanField(label="Crime: ")
    submit = SubmitField(label="Submit")
