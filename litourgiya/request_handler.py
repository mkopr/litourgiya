import requests

from settings import COLLECTOR_REQ_URL, REQUEST_SESSION_VERIFY


class RequestHandler(object):
    BASE_URL = COLLECTOR_REQ_URL

    def __init__(self):
        self.session = requests.Session()
        self.session.verify = REQUEST_SESSION_VERIFY

    def request(self, method='GET', **kwargs):
        url = self._prepare_url(**kwargs)
        method_handler = getattr(self.session, method.lower())
        response = self._request(method_handler, url)
        return self.check_status_code(response)

    @classmethod
    def _request(cls, handler, url):
        url = cls.BASE_URL + url
        return handler(url)

    def prepare_response(self, response):
        try:
            return response.json()
        except Exception:
            return response.text

    def check_status_code(self, response):
        if not response.status_code != 200:
            return self.prepare_response(response)
        return None

    def _prepare_url(self, **kwargs):
        url = f'{kwargs["year"]}/{kwargs["month"]}'
        return url
