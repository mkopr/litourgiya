import random

from flask import request
from flask_restful import Resource

from converters import edit_db_object_from_request
from filters import get_calendars_by_username
from pagination import paginate_data
from serializers import (CalendarEditDataSchema, CalendarResultSchema, DownloadDataRequestSchema,
                         LoginUserRequestSchema, SearchDataRequestSchema)
from services import create_new_user, delete_user_calendars, get_username_from_header, is_user_exists


class LoginUser(Resource):
    """
    Method: POST
    LoginUser view for to login or register users - by name.
    Pass user name in request body.
    Example:
        {'username': 'your_name'}
    """
    def post(self):
        serialized_data = LoginUserRequestSchema().load(request.json)
        if not serialized_data.errors:
            username = serialized_data.data['username']
            if not is_user_exists(username):
                create_new_user(username)
                return {'message': f'created user: {username}'}, 201
            return {'message': f'{username} exists in db'}, 200
        return serialized_data.errors, 400


class DownloadData(Resource):
    """
    Method: GET
    DownloadData view for get data from outside api and put it to celery task and convert to database objects.
    Pass start and end query params with dates. Put username in request header - Authentication Username your_name
    """
    def get(self):
        username = get_username_from_header(request)
        if is_user_exists(username):
            serialized_data = DownloadDataRequestSchema().load(request.args)
            if not serialized_data.errors:
                dates = {'start': request.args['start'], 'end': request.args['end']}
                from app import collect_data  # to solve circular ImportError with Celery
                collect_data.delay(dates, username)
                return {'message': f'Download triggered for dates: {dates}'}, 200
            return serialized_data.errors, 400
        return '', 401


class SearchData(Resource):
    """
    Method: GET
    Get all data related with user.
    Put username in request header - Authentication Username your_name.
    Params: page, size, start, end, weekday, colour

    Method: PUT
    Edit data related with user.
    Put username in request header - Authentication Username your_name.
    To edit calendar set correct date in request body.
    To edit celebration set corrent ID in request body.
    Example:
        {
            "weekday": "thursday",
            "date": "2018-08-02",
            "season_week": 17,
            "celebrations": [
                {
                    "calendar": 9,
                    "rank": "ferial",
                    "rank_num": 3.13,
                    "colour": "green",
                    "id": 15,
                    "title": "Thursday, 17th week in Ordinary Time"
                },
                {
                    "calendar": 9,
                    "rank": "optional memorial",
                    "rank_num": 3.12,
                    "colour": "white",
                    "id": 16,
                    "title": "The most Saint Eusebius of Vercelli, bishop"
                },
            ],
            "season": "non-ordinary"
        }

    Method: DELETE
    Delete all related with user calendars and celebrations.
    Put username in request header - Authentication Username your_name.
    """
    def get(self):
        username = get_username_from_header(request)
        if is_user_exists(username):
            serialized_data = SearchDataRequestSchema().load(request.args)
            if not serialized_data.errors:
                calendars = get_calendars_by_username(username, request.args)
                return paginate_data(CalendarResultSchema(many=True).dump(calendars).data, serialized_data.data), 200
            return serialized_data.errors, 400
        return '', 401

    def put(self):
        username = get_username_from_header(request)
        if is_user_exists(username):
            serialized_data = CalendarEditDataSchema().load(request.json)
            if not serialized_data.errors:
                if not edit_db_object_from_request(request.json, username):
                    return '', 404
                return '', 200
            return serialized_data.errors, 400
        return '', 401

    def delete(self):
        username = get_username_from_header(request)
        if is_user_exists(username):
            if not delete_user_calendars(username):
                return '', 400
            return '', 200
        return '', 401


class RandomData(Resource):
    """
    Method: GET
    Get one random object related with user.
    Put username in request header - Authentication Username your_name.
    """
    def get(self):
        username = get_username_from_header(request)
        if is_user_exists(username):
            calendars = get_calendars_by_username(username, request.args)
            return random.choice(CalendarResultSchema(many=True).dump(calendars).data), 200
        return '', 401
