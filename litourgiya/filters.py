from datetime import datetime

from models import Calendar, db
from settings import date_format


def get_calendars_by_username(username: str, params: dict):
    query = db.session.query(Calendar).join(Calendar.user, aliased=True).filter_by(username=username)
    if not params:
        return query
    if params.get('weekday', None):
        query = query.filter(Calendar.weekday == params['weekday'])
    elif params.get('colour', None):
        query = query.join(Calendar.celebrations, aliased=True).filter_by(colour=params['colour'])
    elif params.get('start', None) and params.get('end', None):
        query = query.filter(
            Calendar.date >= datetime.strptime(params['start'], date_format),
            Calendar.date <= datetime.strptime(params['end'], date_format)
        )
    return query.all()
