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
        allAmenity = [a for a in storage.all('Amenity').values()]
        if storage_t is "FileStorage":
            amenity_ids = place.amenity_id
            amenity = [a.to_dict() for a in allAmenity if a.id in amenity_ids]
        if storage_t is "DBStorage":
            amenity = [a.to_dict() for a in allAmenity if a in place.amenities]
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
        if storage_t == "DBStorage":
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        if storage_t == "FileStorage":
            if amenity.id not in place.amenity_ids:
                abort(404)
            place.amenity_id.remove(amenity.id)

        storage.save()
        return jsonify({}), 200

    if request.method == 'POST':
        place = storage.get(classes["Place"], place_id)
        if place is None:
            abort(404)
        amenity = storage.get(["Amenity"], amenity_id)
        if amenity is None:
            abort(404)

        if storage_t == "File_storage":
            if (amenity.id in place.amenity_ids):
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenity_ids.append(amenity.id)
        else:
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenities.append(amenity)

        return jsonify(amenity.to_dict()), 201
