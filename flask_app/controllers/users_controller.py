from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.place_model import Place
from flask_app.utilities import utilities
bcrypt = Bcrypt(app)

#home page
@app.route('/')
def index():
    places = Place.get_all()
    print('--------the list of all the places-------------------')
    places_dict = [one_place.to_dict() for one_place in places]

    return render_template("home.html", all_places = places_dict)

@app.route('/login/registration')
def registration_page():
    return render_template("index.html")

#register the user
@app.route('/users/register', methods=['POST'])
def reg_user():
    if not User.validator(request.form):
        return redirect('/login/registration')

    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password':hashed_pass,
        'conf_pass': hashed_pass
    }
    session['user_id'] = User.create(data)
    return redirect('/')

#logs in the user
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

#logs out the user
@app.route('/users/logout')
def log_out():
    del session['user_id']
    return redirect('/')

#the dashboard
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        flash("you don't belong there!", "not_logged")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)

    return render_template("dashboard.html",logged_user=logged_user)


