#!/usr/bin/python3
"""Defines the statues of the JSON file returned"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status"""
    status = {"status": "OK"}
    return jsonify(status), 200


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieves the number of each object type"""
    stats = {}
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]

    for cls in classes:
        count = storage.count(cls)
        stats[cls] = count

    return jsonify(stats)
