#!/usr/bin/python3
"""Places module"""
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/cities/<city_id>/places', methods=[
    'GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=[
    'DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=[
    'POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a new Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()

    return jsonify(place.to_dict()), 200
