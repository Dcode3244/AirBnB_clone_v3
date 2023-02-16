#!/usr/bin/python3
"""
handles all RESTFUl API actions for places
"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
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


@app_views.route("/places_search", methods=['POST'])
def place_search_get():
    result = []
    if not request.json:
        return make_response("Not a JSON", 400)
    if not len(request.json):
        task = [task for task in storage.all('Place')]
        return jsonify(task)
    place_T = list(storage.all('Place').values())
    if 'amenities' in request.json:
        place_T = []
        for T in storage.all('Place').values():
            for ament in T.amenities:
                for A_key in request.json['amenities']:
                    if ament.id == A_key:
                        place_T.append(ament)
    if 'states' in request.json and 'cities' not in request.json:
        states = [storage.get(classes["State"], states)
                  for states in request.json['states']]
        for state in states:
            for city in state.cities:
                for i in storage.all("Place").values():
                    if i.city_id == city.id:
                        result.append(i.to_dict())
    elif 'cities' in request.json and 'states' not in request.json:
        cities = request.json['cities']
        for city in cities:
            for i in storage.all("Place").values():
                if i.city_id == city:
                    result.append(i.to_dict())
    else:
        test = []
        states = [storage.get(classes["State"], states)
                  for states in request.json['states']]
        citi = request.json['cities']
        for state in states:
            for city, city_P in zip(state.cities, citi):
                for i in storage.all("Place").values():
                    if i.city_id == city.id or i.city_id == city_P:
                        test.append(i.to_dict())
        result = []
        [result.append(x) for x in test if x not in result]
    return jsonify(result)
