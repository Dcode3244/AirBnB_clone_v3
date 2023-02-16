#!/usr/bin/python3
"""
handles all RESTFUl API actions for places
"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage, storage_t
from models.engine.db_storage import classes


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_by_city_id(city_id):
    """ defines route for api/v1/cities/<city_id>/places """
    city = storage.get(classes['City'], city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        allPlaces = [p for p in storage.all('Place').values()]
        places = [p.to_dict() for p in allPlaces if city_id == p.city_id]
        return jsonify(places)

    if request.method == 'POST':
        if not request.json:
            return make_response('Not a JSON', 400)
        if 'user_id' not in request.json:
            return make_response('Missing user_id', 400)
        user = storage.get(classes['User'], request.json.get('user_id'))
        if user is None:
            abort(404)
        if 'name' not in request.json:
            return make_response('Missing name', 400)
        placeDict = request.json
        placeDict['city_id'] = city_id
        newObj = classes['Place']
        newPlace = newObj(**placeDict)
        newPlace.save()
        return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_by_place_id(place_id):
    """  defines a route to /places/<place_id> """
    allPlace = [p for p in storage.all('Place').values()]
    places = [p for p in allPlace if p.id == place_id]
    if len(places) == 0:
        abort(404)
    if request.method == 'GET':
        return jsonify(places[0].to_dict())

    if request.method == 'DELETE':
        storage.delete(places[0])
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            return make_response('Not a JSON', 400)
        data = request.json
        checkList = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in checkList:
                setattr(places[0], key, value)
                places[0].save()
        return jsonify(places[0].to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
        places route to handle http method for request to search places
    """
    all_places = [p for p in storage.all('Place').values()]
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    states = req_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all('City')
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([
            c_id for c_id in cities if storage.get('City', c_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_dict() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get('Amenity', a_id)])
        for p in all_places:
            p_amenities = None
            if storage_t == 'db' and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p)
    else:
        places_amenities = all_places
    result = [place.to_dict() for place in places_amenities]
    return jsonify(result)
