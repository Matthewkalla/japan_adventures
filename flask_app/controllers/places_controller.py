from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.place_model import Place
from flask_app.utilities import utilities
from flask_app.config import config
import requests
bcrypt = Bcrypt(app)


#the route to go to add a new place
@app.route('/places/add')
def new_place():
    
    return render_template("add_place.html")


#the route to insert the new place into the database
@app.route('/places/create', methods=['POST'])
def add_place():
    print("-----------------the request form")
    print(request.form)

    #validation method
    if not Place.validator(request.form):
        return redirect('/places/add')
    # convert the address into
    #longitude and lattitude to store in the database
    params = {
        'key': config.API_KEY,
        'address': request.form['location']
    }

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params).json()
    
    if response['status'] == 'OK':
        geometry = response['results'][0]['geometry']
        lat = geometry['location']['lat']
        lng = geometry['location']['lng']

    print(f"latitude: {lat}")
    print(f"longitude: {lng}")

    place_data = {
        **request.form,
        'lat': lat,
        'lng': lng,
        'user_id': session['user_id']
    }
    Place.create(place_data)

    return redirect('/')


#the route to view all the pla
@app.route('/places/view')
def view_all_places():
    all_places = Place.get_all()
    return render_template("my_locations.html", all_places=all_places)


#the method to render the edit location form
@app.route('/places/<int:id>/edit')
def view_edit_form(id):
    if 'user_id' not in session:
        return redirect('/')
    
    one_place = Place.get_one({'id':id})

    return render_template("edit_place.html", one_place=one_place)


#the method to update the location
@app.route('/places/<int:id>/update', methods=['POST'])
def edit_place(id):
    if 'user_id' not in session:
        return redirect('/')
    
    if not Place.validator(request.form):
        return redirect(f'/places/{id}/edit')
    place_data = {
        **request.form,
        'id': id
    }
    Place.update(place_data)
    return redirect('/')


#the method to delete the location
@app.route('/places/<int:id>/delete')
def delete(id):
    if 'user_id' not in session:
        return redirect('/')
    Place.delete({'id':id})
    return redirect('/')
