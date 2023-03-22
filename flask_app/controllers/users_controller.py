import googlemaps
from flask_app import app
from flask_app import API_KEY
from flask_bcrypt import Bcrypt
from flask_app.utilities import utilities
from flask_app.models.user_model import User
from flask_app.models.place_model import Place
from flask import render_template, redirect, request, flash, session
bcrypt = Bcrypt(app)

# for translating lat and lng into address
gmaps = googlemaps.Client(API_KEY)


# home page

@app.route('/')
def index():
    places = Place.get_all()

    # iterate over the array and convert to an address from lattitude and longitude
    for place in places:
        temp_address = gmaps.reverse_geocode((place['lat'], place['lng']))
        place['addr'] = temp_address[1]['formatted_address']

    return render_template("home.html", places=places, api_key=API_KEY)


# the route to show the login and registration form

@app.route('/login/registration')
def registration_page():
    return render_template("index.html")


# register the user

@app.route('/users/register', methods=['POST'])
def reg_user():
    if not User.validator(request.form):
        return redirect('/login/registration')

    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pass,
        'conf_pass': hashed_pass
    }
    session['user_id'] = User.create(data)
    return redirect('/')


# logs in the user

@app.route('/users/login', methods=['POST'])
def log_user():
    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash("invalid credentials", "log")
        return redirect('/login/registration')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("invalid credentials", "log")
        return redirect('/login/registration')
    session['user_id'] = user_in_db.id
    return redirect('/')


# logs out the user

@app.route('/users/logout')
def log_out():
    del session['user_id']
    return redirect('/')
