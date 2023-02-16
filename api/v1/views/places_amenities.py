#!/usr/bin/python3
"""
handles all default RESTFul API actions:
"""

from models import storage, storage_t
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models.engine.db_storage import classes


@app_views.route('/places/<place_id>/amenities', methods=["GET"])
def get_amenities_by_place(place_id):
    """ defines route to api/v1/places/<place_id>/amenities """
    if request.method == 'GET':
        place = storage.get(classes['Place'], place_id)
        if not place:
            abort(404)
        amenity = [a.to_dict() for a in place.amenities]
        return jsonify(amenity)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=["DELETE", "POST"])
def handle_amenities_by_id(place_id, amenity_id):
    """ defines route to api/v1/places/<place_id>/amenities/<amenity_id> """
    if request.method == 'DELETE':
        place = storage.get(classes['Place'], place_id)
        if not place:
            abort(404)
        amenity = storage.get(classes['Amenity'], amenity_id)
        if (not amenity):
            abort(404)
        if storage_t == 'db':
            amenities = place.amenities
            a = amenity
        else:
            amenities = place.amenity_id
            a = amenity.id
        for i in range(len(amenities)):
            if amenities[i] == a:
                amenities.pop(i)
                storage.save()
                return jsonify({}), 200
        abort(404)

    if request.method == 'POST':
        place = storage.get(classes["Place"], place_id)
        if place is None:
            abort(404)
        amenity = storage.get(["Amenity"], amenity_id)
        if amenity is None:
            abort(404)

        if storage_t == "db":
            amenities = place.amenities
        else:
            amenities = place.amenity_id
        for a in amenities:
            if (a == amenity):
                return jsonify(a.to_dict()), 200

        place.amenities.append(amenity)
        amenity.save()
        return jsonify(amenity.to_dict()), 201
