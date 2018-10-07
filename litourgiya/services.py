from datetime import datetime, timedelta

from models import Calendar, Celebration, User, db
from request_handler import RequestHandler
from settings import date_format


def is_user_exists(username: str) -> bool:
    if not User.query.filter_by(username=username).first():
        return False
    return True


def create_new_user(username: str) -> User:
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def delete_user_calendars(username: str) -> bool:
    try:
        user = User.query.filter_by(username=username).first()
        calendar = db.session.query(Calendar).filter(Calendar.user == user)
        calendar.delete()
        db.session.commit()
        return True
    except Exception as e:
        return False


def update_calendar(calendar: Calendar, data: dict) -> Calendar:
    if data.get('season', None):
        calendar.season = data['season']
    if data.get('season_week', None):
        calendar.season_week = data['season_week']
    if data.get('weekday', None):
        calendar.weekday = data['weekday']
    db.session.commit()
    return calendar


def create_new_calendar(user: User, data: dict) -> Calendar:
    new_calendar = Calendar(
        user=user,
        date=datetime.strptime(data['date'], date_format),
        season=data['season'],
        season_week=data['season_week'],
        weekday=data['weekday']
    )
    db.session.add(new_calendar)
    db.session.commit()
    return new_calendar


def update_celebration(celebration: Celebration, data: dict) -> Celebration:
    if data.get('title', None):
        celebration.title = data['title']
    if data.get('colour', None):
        celebration.colour = data['colour']
    if data.get('rank', None):
        celebration.rank = data['rank']
    if data.get('rank_num', None):
        celebration.rank_num = data['rank_num']
    db.session.commit()
    return celebration


def create_new_celebration(calendar: Calendar, data: dict) -> Celebration:
    new_celebration = Celebration(
        calendar=calendar,
        title=data['title'],
        colour=data['colour'],
        rank=data['rank'],
        rank_num=data['rank_num']
    )
    db.session.add(new_celebration)
    db.session.commit()
    return new_celebration


def get_all_dates_between(dates: dict) -> list:
    start_date = datetime.strptime(dates['start'], date_format)
    end_date = datetime.strptime(dates['end'], date_format)
    delta = end_date - start_date
    return [start_date + timedelta(date) for date in range(delta.days + 1)]


def get_year_and_month_from_dates(dates: list) -> list:
    return set([(date.year, date.month) for date in dates])


def get_username_from_header(request) -> str:
    return request.headers.get('Authorization', '').replace('Username ', '')


def get_data_per_month(date: tuple) -> list:
    handler = RequestHandler()
    return handler.request(year=date[0], month=date[1])
