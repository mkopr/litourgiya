from unittest.mock import patch

from app import collect_data
from utils import CallableMock, get_random_colour, get_random_string, get_random_weekday


class TestUnknown:
    def test_unknown_url(self, client):
        response = client.get('/')
        assert 404 == response.status_code


class TestLoginUserView:
    def test_login_new_user(self, client, username=None):
        if not username:
            username = get_random_string()
        body = {'username': username}
        response = client.post('/api/login', json=body)
        assert 201 == response.status_code
        assert {'message': f'created user: {username}'} == response.json

    def test_check_logged_user(self, client):
        username = get_random_string()
        body = {'username': username}
        self.test_login_new_user(client, username)
        response = client.post('/api/login', json=body)
        assert 200 == response.status_code
        assert {'message': f'{username} exists in db'} == response.json

    def test_invalid_request_body(self, client):
        username = get_random_string()
        body = {'nick': username}
        response = client.post('/api/login', json=body)
        assert 400 == response.status_code
        assert {'username': ['Missing data for required field.']} == response.json


class TestDownloadDataView:
    def test_unauthorized_request(self, client):
        response = client.get('/api/download')
        assert 401 == response.status_code

    def test_invalid_request_required_fields(self, client):
        username = get_random_string()
        body = {'username': username}
        headers = {'Authorization': f'Username {username}'}

        client.post('/api/login', json=body)
        response = client.get('/api/download', headers=headers)
        assert 400 == response.status_code
        assert {
                   'end': ['Missing data for required field.'], 'start': ['Missing data for required field.']
               } == response.json

    @patch('app.collect_data.delay', CallableMock)
    def test_correct_request(self, client):
        username = get_random_string()
        body = {'username': username}
        headers = {'Authorization': f'Username {username}'}
        dates = {'start': '2018-09-01', 'end': '2018-10-01'}

        client.post('/api/login', json=body)
        response = client.get('/api/download', headers=headers, query_string=dates)
        assert 200 == response.status_code
        assert {'message': f'Download triggered for dates: {dates}'} == response.json


class TestGetSearchData:
    def test_unauthorized_request(self, client):
        response = client.get('/api/search')
        assert 401 == response.status_code

    def test_invalid_request_params(self, client):
        username = get_random_string()
        body = {'username': username}
        headers = {'Authorization': f'Username {username}'}
        params = {'start': 20180901, 'end': 20181001, 'weekday': 1, 'colour': 2, 'page': 'one', 'size': 'big'}

        client.post('/api/login', json=body)
        response = client.get('/api/search', headers=headers, query_string=params)
        assert 400 == response.status_code
        assert {
                   'end': ['Not a valid date.'],
                   'page': ['Not a valid integer.'],
                   'size': ['Not a valid integer.'],
                   'start': ['Not a valid date.']
               } == response.json

    @patch('app.collect_data.delay', collect_data.run)
    def test_search_all_data(self, client):
        username = get_random_string()
        body = {'username': username}
        headers = {'Authorization': f'Username {username}'}
        dates = {'start': '2018-09-01', 'end': '2018-09-30'}

        client.post('/api/login', json=body)
        client.get('/api/download', headers=headers, query_string=dates)
        response = client.get('/api/search', headers=headers)
        assert 200 == response.status_code
        for key in ['count', 'data', 'page', 'size']:
            assert key in response.json.keys()

    @patch('app.collect_data.delay', collect_data.run)
    def test_search_by_weekday(self, client):
        username = get_random_string()
        body = {'username': username}
        headers = {'Authorization': f'Username {username}'}
        dates = {'start': '2018-09-01', 'end': '2018-09-30'}
        weekday = get_random_weekday()
        params = {'weekday': weekday}

        client.post('/api/login', json=body)
        client.get('/api/download', headers=headers, query_string=dates)
        response = client.get('/api/search', headers=headers, query_string=params)
        assert 200 == response.status_code
        for day in response.json.get('data', {}):
            assert weekday == day.get('weekday', None)

    @patch('app.collect_data.delay', collect_data.run)
    def test_search_by_colour(self, client):
        username = get_random_string()
        body = {'username': username}
        headers = {'Authorization': f'Username {username}'}
        dates = {'start': '2018-09-01', 'end': '2018-09-30'}
        colour = get_random_colour()
        params = {'colour': colour}

        client.post('/api/login', json=body)
        client.get('/api/download', headers=headers, query_string=dates)
        response = client.get('/api/search', headers=headers, query_string=params)
        assert 200 == response.status_code
        for day in response.json.get('data', {}):
            for celebration in day.get('celebration', {}):
                colours = [colour for colour in celebration.get('colour', None)]
                assert colour in colours


class TestEditData:
    def test_unauthorized_request(self, client):
        response = client.put('/api/search')
        assert 401 == response.status_code

    def test_invalid_request_params(self, client):
        username = get_random_string()
        body = {'username': username}
        headers = {'Authorization': f'Username {username}'}
        edit_data = {'date': 20180901, 'weekday': 1, 'season_week': 'two'}

        client.post('/api/login', json=body)
        response = client.put('/api/search', headers=headers, json=edit_data)
        assert 400 == response.status_code
        assert {
                   'date': ['Not a valid date.'],
                   'season_week': ['Not a valid integer.'],
                   'weekday': ['Not a valid string.']
               } == response.json

    @patch('app.collect_data.delay', collect_data.run)
    def test_not_found_edit_request(self, client):
        username = get_random_string()
        body = {'username': username}
        headers = {'Authorization': f'Username {username}'}
        dates = {'start': '2018-09-01', 'end': '2018-09-30'}
        edit_data = {'date': '2019-09-01', 'season_week': 999}

        client.post('/api/login', json=body)
        client.get('/api/download', headers=headers, query_string=dates)
        response = client.put('/api/search', headers=headers, json=edit_data)
        assert 404 == response.status_code

    @patch('app.collect_data.delay', collect_data.run)
    def test_valid_edit_request(self, client):
        new_season_week = 999
        username = get_random_string()
        body = {'username': username}
        headers = {'Authorization': f'Username {username}'}
        dates = {'start': '2018-09-01', 'end': '2018-09-30'}
        edit_data = {'date': '2018-09-01', 'season_week': new_season_week}

        client.post('/api/login', json=body)
        client.get('/api/download', headers=headers, query_string=dates)
        response = client.put('/api/search', headers=headers, json=edit_data)
        assert 200 == response.status_code

        response = client.get('/api/search', headers=headers)
        assert new_season_week in [day.get('season_week', None) for day in response.json.get('data', {})]


class TestDeleteData:
    def test_unauthorized_request(self, client):
        response = client.delete('/api/search')
        assert 401 == response.status_code

    @patch('app.collect_data.delay', collect_data.run)
    def test_delete(self, client):
        username = get_random_string()
        body = {'username': username}
        headers = {'Authorization': f'Username {username}'}
        dates = {'start': '2018-09-01', 'end': '2018-09-30'}

        client.post('/api/login', json=body)
        client.get('/api/download', headers=headers, query_string=dates)
        response = client.get('/api/search', headers=headers)
        assert 200 == response.status_code
        assert 0 < response.json.get('count', None)

        response = client.delete('/api/search', headers=headers)
        assert 200 == response.status_code

        response = client.get('/api/search', headers=headers)
        assert 200 == response.status_code
        assert 0 == response.json.get('count', None)


class TestRandomData:
    def test_unauthorized_request(self, client):
        response = client.put('/api/random')
        assert 401 == response.status_code

    @patch('app.collect_data.delay', collect_data.run)
    def test_get_random(self, client):
        username = get_random_string()
        body = {'username': username}
        headers = {'Authorization': f'Username {username}'}
        dates = {'start': '2018-09-01', 'end': '2018-09-30'}

        client.post('/api/login', json=body)
        client.get('/api/download', headers=headers, query_string=dates)
        response = client.get('/api/search', headers=headers)
        assert 200 == response.status_code
        assert 0 < response.json.get('count', None)

        response = client.get('/api/random', headers=headers)
        assert 200 == response.status_code
        assert None is response.json.get('data', None)
        assert 7 == len(response.json)  # number of CalendarEditDataSchema fields
