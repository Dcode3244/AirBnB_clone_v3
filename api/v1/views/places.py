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
def place_search():
    """ POST method to search a place bases in json body"""
    if not request.is_json:
        abort(400, "Not a JSON")
    parms = request.get_json()
    vals = [len(item) for item in parms.values()]
    if ((len(parms) is 0) or (max(vals) is 0)):
        places = storage.all("Place").values()
        return jsonify([item.to_dict() for item in places])
    places = []
    places_obj = []
    if 'states' in parms and len(parms.get('states')) > 0:
        states = parms.get('states')
        states_obj = [storage.get('State', state) for state in states]
        for state_obj in states_obj:
            state_cities = state_obj.cities
            for city in state_cities:
                city_places = city.places
                for place in city_places:
                    places.append(place.to_dict())
                    places_obj.append(place)
    if 'cities' in parms and len(parms.get('cities')) > 0:
        cities = parms.get('cities')
        cities_obj = [storage.get('City', city) for city in cities]
        for city in cities_obj:
            city_places = city.places
            for place in city_places:
                places.append(place.to_dict())
                places_obj.append(place)
    if 'amenities' in parms and len(parms.get('amenities')) > 0:
        amenities = parms.get('amenities')
        amenities_obj = [storage.get('Amenity', amenity)
                         for amenity in amenities]
        print(places_obj)
        if len(places_obj) == 0:
            places_obj = storage.all('Place').values()
        else:
            places = []
        for place in places_obj:
            amenity_place = []
            amenities2 = place.amenities
            for amenity2 in amenities2:
                amenity_place.append(amenity2.id)
            for amenity in amenities:
                if amenity in amenity_place:
                    flag = True
                else:
                    flag = False
                    break
            if flag is True:
                place2 = place.to_dict()
                del place2['amenities']
                places.append(place2)
    places = [i for n, i in enumerate(places) if i not in places[n + 1:]]
    return jsonify(places)

# @app_views.route("/places_search", methods=['POST'])
# def place_search_get():
#    result = []
#    if not request.json:
#        return make_response("Not a JSON", 400)
#    if not len(request.json):
#        task = [task for task in storage.all('Place')]
#        return jsonify(task)
#    place_T = list(storage.all('Place').values())
#    if 'amenities' in request.json:
#        place_T = []
#        for T in storage.all('Place').values():
#            for ament in T.amenities:
#                for A_key in request.json['amenities']:
#                    if ament.id == A_key:
#                        place_T.append(ament)
#    if 'states' in request.json and 'cities' not in request.json:
#        states = [storage.get(classes["State"], states)
#                  for states in request.json['states']]
#        for state in states:
#            for city in state.cities:
#                for i in storage.all("Place").values():
#                    if i.city_id == city.id:
#                        result.append(i.to_dict())
#    elif 'cities' in request.json and 'states' not in request.json:
#        cities = request.json['cities']
#        for city in cities:
#            for i in storage.all("Place").values():
#                if i.city_id == city:
#                    result.append(i.to_dict())
#    elif ('states' in request.json and 'cities' in request.json):
#        test = []
#        states = [storage.get(classes["State"], states)
#                  for states in request.json.get('states')]
#        citi = request.json['cities']
#        for state in states:
#            for city, city_P in zip(state.cities, citi):
#                for i in storage.all("Place").values():
#                    if i.city_id == city.id or i.city_id == city_P:
#                        test.append(i.to_dict())
#        result = []
#        [result.append(x) for x in test if x not in result]
#    return jsonify(result)
