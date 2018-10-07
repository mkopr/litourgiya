import os

# DATE
date_format = '%Y-%m-%d'

# DATABASE
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "litourgiya.db"))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# COLLECTOR
COLLECTOR_REQ_URL = 'http://calapi.inadiutorium.cz/api/v0/en/calendars/general-en/'
REQUEST_SESSION_VERIFY = True

# PAGINATION
DEFAULT_PAGE_SIZE = 20

# REDIS
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')

# CELERY
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BROKER_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
