from flask import render_template, redirect, url_for, flash, request
from tickets import app, db
from tickets.forms import registerForm, LoginForm, addVenue, addShow, BookTickets, Search, ReviewForm, GenreForm
from tickets.models import User, Venue, Show, Tickets, Reviews, Genre
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/dashboard')
@login_required
def dashBoard_page():
    venues = Venue.query.all()
    return render_template('dashboard.html', venues=venues)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = registerForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email_address=form.email.data, password=form.password1.data,
                    is_admin=form.isAdmin.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Account Created Successfully and Logged in', category='success')
        return redirect(url_for('dashBoard_page'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"There was an error, {err}", category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(username=form.username.data).first()
        if user_exists:
            if user_exists.check_password(form.password.data):
                login_user(user_exists)
                flash("Logged in Successfully!", category='success')
                return redirect(url_for('dashBoard_page'))
            else:
                flash("Username and Password does not Match", category='danger')
        else:
            # print(user_exists.check_password(form.password.data))
            flash("Username does not exist, please register", category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("Successfully Logged out", category='info')
    return redirect(url_for('login_page'))


@app.route('/add-venue', methods=['GET', 'POST'])
@login_required
def add_venue_page():
    form = addVenue()
    if form.validate_on_submit():
        venue_exists = Venue.query.filter_by(venue_name=form.username.data).first()
        if not venue_exists:
            newVenue = Venue(venue_name=form.username.data, venue_address=form.venueaddress.data)
            db.session.add(newVenue)
            db.session.commit()
            flash("Venue added successfully", category="success")
            return redirect(url_for('dashBoard_page'))
        else:
            flash("Venue Already Exists", category="danger")
    if form.errors != {}:
        flash("There was an Error", category="danger")
    return render_template('addVenue.html', form=form)


@app.route('/venue/<name>-<id>')
@login_required
def venue_page(name, id):
    shows = Show.query.filter_by(at_venue=id).order_by(Show.id.desc())
    show2 = []
    for show in shows:
        genre = Genre.query.filter_by(show_id=show.id).all()
        show2.append([show, genre])
    venue = Venue.query.filter_by(venue_name=name).first()
    return render_template('venue.html', venue=venue, show=show2)


@app.route('/add-show/<name>-<id>', methods=['GET', 'POST'])
@login_required
def add_show_page(name, id):
    form = addShow()
    if form.validate_on_submit():
        newShow = Show(show_name=form.show_name.data,
                       show_timings=form.show_timings.data,
                       rating=form.rating.data,
                       ticket_rate=form.ticket_rate.data,
                       at_venue=id,
                       no_of_seats=form.no_of_seats.data,
                       img_url=form.img_url.data,
                       category=form.category.data,
                       lang=form.lang.data)
        db.session.add(newShow)
        db.session.commit()
        show = Show.query.filter_by(at_venue=id, show_name=form.show_name.data).all()[-1]
        flash("Show Added Successfully", category='success')
        return redirect(url_for('add_genre', showid=show.id))
    if form.errors != {}:
        flash("There was an Error", category="danger")
    return render_template('addShow.html', form=form)


@app.route('/del/venue/<id>')
@login_required
def delete_venue_page(id):
    venue_to_del = Venue.query.filter_by(id=id).first()
    shows_to_del = Show.query.filter_by(at_venue=id).delete()
    db.session.commit()
    db.session.delete(venue_to_del)
    db.session.commit()
    return redirect(url_for('dashBoard_page'))


@app.route('/update/venue/<id>', methods=['GET', 'POST'])
@login_required
def update_venue_page(id):
    form = addVenue()
    venue = Venue.query.filter_by(id=id).first()
    form.submit.label.text = "Update"
    form.venueaddress.data = venue.venue_address
    form.username.data = venue.venue_name
    if form.validate_on_submit() and request.method == 'POST':
        venue.venue_name = request.form['username']
        venue.venue_address = request.form['venueaddress']
        db.session.commit()
        return redirect(url_for("dashBoard_page"))

    return render_template('addVenue.html', form=form, venue=venue)


@app.route('/delete/show/<name>-<id1>/<id2>')
@login_required
def delete_show_page(name, id1, id2):
    show_to_del = Show.query.filter_by(id=id2).first()
    db.session.delete(show_to_del)
    db.session.commit()
    return redirect(url_for('venue_page', name=name, id=id1))


@app.route('/update/show/<name>-<id1>/<id2>', methods=['GET', 'POST'])
@login_required
def update_show_page(name, id1, id2):
    form = addShow()
    form.submit.label.text = "Next"
    show = Show.query.filter_by(id=id2).first()
    form.show_name.data = show.show_name
    form.show_timings.data = show.show_timings
    form.rating.data = show.rating
    form.ticket_rate.data = show.ticket_rate
    form.no_of_seats.data = show.no_of_seats
    form.img_url.data = show.img_url
    form.category.data = show.category
    form.lang.data = show.lang

    if form.validate_on_submit() and request.method == 'POST':
        show.show_name = request.form['show_name']
        show.show_timings = request.form['show_timings']
        show.rating = request.form['rating']
        show.ticket_rate = request.form['ticket_rate']
        show.no_of_seats = request.form['no_of_seats']
        show.img_url = request.form['img_url']
        show.category = request.form['category']
        show.lang = request.form['lang']
        db.session.commit()
        return redirect(url_for('add_genre', showid=id2))
    return render_template('addShow.html', form=form, update=True)


@app.route('/bookTikets/<showid>', methods=['GET', 'POST'])
@login_required
def book_tickets_page(showid):
    show = Show.query.filter_by(id=showid).first()
    user = User.query.filter_by(id=current_user.id).first()
    form = BookTickets()
    if form.validate_on_submit() and request.method == 'POST':
        if int(show.no_of_seats) >= int(form.tickets.data) and int(show.no_of_seats) > 0:
            if int(show.ticket_rate) * int(form.tickets.data) <= current_user.budget:
                tickets = Tickets(show_id=showid, no_of_tickets=form.tickets.data, username=current_user.username)
                db.session.add(tickets)
                db.session.commit()
                user.budget = current_user.budget - float(show.ticket_rate) * float(form.tickets.data)
                show.no_of_seats = str(int(show.no_of_seats) - int(form.tickets.data))
                db.session.commit()
                flash("Tickets Booked successfully", category="success")
                return redirect(url_for('dashBoard_page'))
            else:
                flash("Not enough budget", category="danger")
        else:
            flash("Only {} seats are available".format(show.no_of_seats), category="danger")
    if form.errors != {}:
        flash("Validation error", category="danger")
    return render_template('BookTickets.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search_page():
    form = Search()
    if form.validate_on_submit() and request.method == 'POST':
        shows = Show.query.filter_by(show_name=form.search.data).all()
        venues = Venue.query.filter_by(venue_name=form.search.data).all()
        genre = Genre.query.filter_by(genre=form.search.data).all()
        # print(shows, venues, genre)
        showbyGenre = []
        for gen in genre:
            show = Show.query.filter_by(id=gen.show_id).first()
            showbyGenre.append(show)
        return render_template('search.html', form=form, shows=shows, venues=venues, showbyGenre=showbyGenre)
    return render_template('search.html', form=form)


@app.route('/addReview/<showid>', methods=['GET', 'POST'])
@login_required
def add_review_page(showid):
    form = ReviewForm()
    if form.validate_on_submit() and request.method == 'POST':
        review = Reviews(show_id=showid, review=form.review.data, rating=form.rating.data,
                         username=current_user.username)
        db.session.add(review)
        db.session.commit()
        flash("Review Added Successfully, Thankyou for the response", category="success")
        return redirect(url_for('see_review_page', showid=showid))
    if form.errors != {}:
        flash("An Error Occurred", category="danger")
    return render_template('addReview.html', form=form)


# @app.route('/delreview', methods=['GET', 'POST'])
# @login_required
# def del_review():
#     # # get the column instance from table object
#     # my_col_instance = [col for col in Reviews._columns if col.name == "review"][0]
#     # # remove from the ColumnCollection, note that we're removing it from ._columns not .columns
#     # Reviews._columns.remove(my_col_instance)
#     # # execute actual ALTER TABLE SQL query to drop the column
#     # delattr(Reviews, 'review')
#     del Reviews.__mapper__._props["review"]
#     return redirect(url_for('home_page'))


@app.route('/see/reviews/<showid>')
@login_required
def see_review_page(showid):
    reviews = Reviews.query.filter_by(show_id=showid).all()
    return render_template('seeReview.html', reviews=reviews)


@app.route('/bookings')
@login_required
def your_bookings():
    tickets = Tickets.query.filter_by(username=current_user.username).all()
    shows = []
    for ticket in tickets:
        show = Show.query.filter_by(id=ticket.show_id).first()
        shows.append([ticket, show])
    return render_template('bookings.html', shows=shows)


@app.route('/bookings/cancel/<bid>')
@login_required
def cancel_booking(bid):
    user = User.query.filter_by(id=current_user.id).first()
    book_to_del = Tickets.query.filter_by(id=bid).first()
    show = Show.query.filter_by(id=book_to_del.show_id).first()
    show.no_of_seats = str(int(show.no_of_seats) + int(book_to_del.no_of_tickets))
    user.budget = current_user.budget + int(show.ticket_rate) * int(book_to_del.no_of_tickets)
    db.session.delete(book_to_del)
    db.session.commit()
    return redirect(url_for('your_bookings'))


@app.route('/addGen/<showid>', methods=['GET', 'POST'])
@login_required
def add_genre(showid):
    form = GenreForm()
    show = Show.query.filter_by(id=showid).first()
    venue = Venue.query.filter_by(id=show.at_venue).first()
    genre = Genre.query.filter_by(show_id=showid).all()
    # print('gen', genre)
    if genre:
        for gen in genre:
            db.session.delete(gen)
        db.session.commit()
    if form.validate_on_submit() and request.method == 'POST':
        for val in form:
            if val.data == True and val.label.text != "Submit":
                gen = val.label.text[0:-2]
                genre = Genre(show_id=showid, genre=gen, venue_id=venue.id)
                db.session.add(genre)
        db.session.commit()
        flash("Genre added successfully", category="success")
        return redirect(url_for('venue_page', name=venue.venue_name, id=venue.id))
    if form.errors != {}:
        flash("An Error Occurred", category="danger")
    return render_template('addGenre.html', form=form)


@app.route('/profile/<username>')
@login_required
def profile_page(username):
    return render_template('profile.html')
