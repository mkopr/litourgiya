from celery import Celery
from flask import Flask
from flask_restful import Api

from converters import create_db_objects_from_data
from models import db
from serializers import ma
from services import get_all_dates_between, get_data_per_month, get_year_and_month_from_dates
from settings import database_file
from views import DownloadData, LoginUser, RandomData, SearchData

api = Api()


def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app() -> Flask:
    # INTI APP
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('settings')
    app.config.from_pyfile('settings.py', silent=True)

    # INIT DB
    app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    with app.app_context():
        db.init_app(app)
        db.create_all()

    # INIT third party
    api.init_app(app)
    ma.init_app(app)

    # DONE
    return app


# URLs
api.add_resource(LoginUser, '/api/login')
api.add_resource(DownloadData, '/api/download')
api.add_resource(SearchData, '/api/search')
api.add_resource(RandomData, '/api/random')

# CELERY
app = create_app()
celery = make_celery(app)


@celery.task()
def collect_data(dates: dict, username: str) -> list:
    # to solve circular ImportError with Celery
    dates = get_all_dates_between(dates)
    months = get_year_and_month_from_dates(dates)
    data = [get_data_per_month(month) for month in months]
    create_db_objects_from_data(data, username, dates)
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
