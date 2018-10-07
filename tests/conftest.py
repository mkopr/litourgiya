import os
import tempfile

import pytest
from app import app
from models import db


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.init_app(app)
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
