#!/usr/bin/python3
"""
handles all RESTFUl API actions for reviews
"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.engine.db_storage import classes


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews_by_place_id(place_id):
    """ defines route for api/v1/place/<place_id>/reviews """
    place = storage.get(classes['Place'], place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        allReviews = [r for r in storage.all('Review').values()]
        reviews = [r.to_dict() for r in allReviews if place_id == r.place_id]
        return jsonify(reviews)

    if request.method == 'POST':
        if not request.json:
            return make_response('Not a JSON', 400)
        if 'user_id' not in request.json:
            return make_response('Missing user_id', 400)
        user = storage.get(classes['User'], request.json.get('user_id'))
        if user is None:
            abort(404)
        if 'text' not in request.json:
            return make_response('Missing text', 400)
        reviewDict = request.json
        reviewDict['place_id'] = place_id
        newObj = classes['Review']
        newReview = newObj(**reviewDict)
        newReview.save()
        return jsonify(newReview.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def reviews_by_review_id(review_id):
    """  defines a route to /reviews/<review_id> """
    allReview = [r for r in storage.all('Review').values()]
    review = [r for r in allReview if r.id == review_id]
    if len(review) == 0:
        abort(404)
    if request.method == 'GET':
        return jsonify(review[0].to_dict())

    if request.method == 'DELETE':
        storage.delete(review[0])
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            return make_response('Not a JSON', 400)
        data = request.json
        checkList = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in checkList:
                setattr(review[0], key, value)
                review[0].save()
        return jsonify(review[0].to_dict()), 200
