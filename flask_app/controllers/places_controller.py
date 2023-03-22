import requests
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

# the route to go to add a new place
@app.route('/places/add')
def new_place():

    return render_template("add_place.html")


# the route to insert the new place into the database
@app.route('/places/create', methods=['POST'])
def add_place():
    print("-----------------the request form")
    print(request.form)

    # validation method
    if not Place.validator(request.form):
        return redirect('/places/add')

    # convert the address into
    # longitude and lattitude to store in the database
    trans_location = utilities.convert_address(request.form['location'])

    place_data = {
        **request.form,
        'lat': trans_location['lat'],
        'lng': trans_location['lng'],
        'user_id': session['user_id']
    }
    Place.create(place_data)

    return redirect('/')


# the route to view all the places
@app.route('/places/view')
def view_all_places():
    all_places = Place.get_all()
    for place in all_places:
        temp_address = gmaps.reverse_geocode((place['lat'], place['lng']))
        place['addr'] = temp_address[1]['formatted_address']
    return render_template("all_locations.html", all_places=all_places)


# route to view one place
@app.route('/places/<int:id>/view')
def view_one_place(id):
    one_place = Place.get_one({'id': id})
    
    #translate lat and lng into a readable address
    temp_address = gmaps.reverse_geocode((one_place.lat, one_place.lng))
    one_place.addr = temp_address[1]['formatted_address']
    return render_template("one_place.html", one_place=one_place)


# the method to render the edit location form
@app.route('/places/<int:id>/edit')
def view_edit_form(id):
    if 'user_id' not in session:
        return redirect('/')

    one_place = Place.get_one({'id': id})
    #translate lat and lng into a readable address
    temp_address = gmaps.reverse_geocode((one_place.lat, one_place.lng))
    one_place.addr = temp_address[1]['formatted_address']

    return render_template("edit_place.html", one_place=one_place)


# the method to update the location
@app.route('/places/<int:id>/update', methods=['POST'])
def edit_place(id):

    #find one place to compare it to the user id; if not equal, redirect
    one_place = Place.get_one({'id': id})

    if 'user_id' != one_place.user_id:
        return redirect('/')

    if not Place.validator(request.form):
        return redirect(f'/places/{id}/edit')
    
    # convert the address into
    # longitude and lattitude to store in the database
    trans_location = utilities.convert_address(request.form['location'])
    place_data = {
        **request.form,
        'lat': trans_location['lat'],
        'lng': trans_location['lng'],
        'id': id
    }
    Place.update(place_data)
    return redirect('/')


# the method to delete the location
@app.route('/places/<int:id>/delete')
def delete(id):

    #find one place to compare it to the user id; if not equal, redirect
    one_place = Place.get_one({'id': id})

    if 'user_id' != one_place.user_id:
        return redirect('/')

    Place.delete({'id': id})
    return redirect('/')
