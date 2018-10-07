from flask_marshmallow import Marshmallow
from marshmallow import fields

from models import Calendar, Celebration
from settings import date_format

ma = Marshmallow()


class LoginUserRequestSchema(ma.Schema):
    username = fields.Str(required=True)


class DownloadDataRequestSchema(ma.Schema):
    start = fields.Date(date_format, required=True)
    end = fields.Date(date_format, required=True)


class SearchDataRequestSchema(ma.Schema):
    start = fields.Date(date_format)
    end = fields.Date(date_format)
    weekday = fields.Str()
    color = fields.Str()
    page = fields.Int()
    size = fields.Int()


class CelebrationResultSchema(ma.ModelSchema):
    class Meta:
        model = Celebration


class CalendarResultSchema(ma.ModelSchema):
    class Meta:
        model = Calendar
    celebrations = fields.Nested(CelebrationResultSchema, many=True)


class CelebrationEditDataSchema(ma.Schema):
    id = fields.Int(required=True)
    calendar = fields.Int()
    rank = fields.Str()
    rank_num = fields.Int()
    colour = fields.Str()
    title = fields.Str()


class CalendarEditDataSchema(ma.Schema):
    date = fields.Date(date_format, required=True)
    weekday = fields.Str()
    season_week = fields.Int()
    celebrations = fields.Nested(CelebrationEditDataSchema, many=True)
