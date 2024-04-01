#!/usr/bin/python3
"""Defines the statues of the JSON file returned"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status"""
    status = {"status": "OK"}
    return jsonify(status), 200
