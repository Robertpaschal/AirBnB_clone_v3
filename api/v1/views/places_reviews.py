#!/usr/bin/python3
"""Places reviews module"""
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=[
    'GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=[
    'DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=[
    'POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a new Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'text' not in data:
        abort(400, description="Missing text")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in [
                'id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()

    return jsonify(review.to_dict()), 200
