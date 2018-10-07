from datetime import datetime

from models import Calendar, Celebration, User, db
from services import create_new_calendar, create_new_celebration, update_calendar, update_celebration
from settings import date_format


def create_db_objects_from_data(months: list, username: str, dates: list) -> None:
    for data in months:
        for date in data:
            if datetime.strptime(date.get('date', None), date_format) in dates:
                calendar = db.session.query(Calendar).filter_by(
                    date=datetime.strptime(date['date'], date_format)
                ).join(Calendar.user).filter_by(username=username).first()
                if not calendar:
                    user = User.query.filter_by(username=username).first()
                    calendar = create_new_calendar(user, date)
                create_celebrations_from_data(date['celebrations'], calendar)


def edit_db_object_from_request(data: dict, username: str) -> bool:
    calendar = db.session.query(Calendar).filter_by(
        date=datetime.strptime(data['date'], date_format)
    ).join(Calendar.user).filter_by(username=username).first()
    if not calendar:
        return False
    update_calendar(calendar, data)
    if data.get('celebrations', None):
        for celebration_data in data['celebrations']:
            celebration = Celebration.query.filter_by(
                id=celebration_data['id']
            ).filter_by(calendar=calendar).first()
            if celebration:
                update_celebration(celebration, celebration_data)
    return True


def create_celebrations_from_data(data: list, calendar: Calendar) -> None:
    for celebration_data in data:
        celebration = Celebration.query.filter_by(calendar=calendar, title=celebration_data['title']).first()
        if not celebration:
            create_new_celebration(calendar, celebration_data)
