import requests
import simplejson as json

from .amplia_error import AmpliaError
from .order_locked_error import OrderLockedError
from .rest_error import RestError
from .rest_unreachable_error import RestUnreachableError


class HttpMethods:
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'


class RestClient(object):

    def __init__(self, endpoint, api_key, custom_headers=None):
        self.__endpoint = endpoint
        self.__api_key = api_key
        self.__custom_headers = custom_headers if (custom_headers is not None) else {}

    def get(self, url):
        _, headers = self.__get_request_params()
        request_url = requests.compat.urljoin(self.__endpoint, url)
        try:
            response = requests.get(request_url, headers=headers)
        except Exception:
            raise RestUnreachableError(HttpMethods.GET, url)

        RestClient.__check_response(HttpMethods.GET, url, response)
        return response.json()

    def post(self, url, data):
        model, headers = self.__get_request_params(data)
        request_url = requests.compat.urljoin(self.__endpoint, url)
        try:
            response = requests.post(request_url, headers=headers, data=json.dumps(model))
        except Exception:
            raise RestUnreachableError(HttpMethods.POST, url)

        RestClient.__check_response(HttpMethods.POST, url, response)
        return response.json()

    def delete(self, url):
        _, headers = self.__get_request_params()
        request_url = requests.compat.urljoin(self.__endpoint, url)
        try:
            response = requests.delete(request_url, headers=headers)
        except Exception:
            raise RestUnreachableError(HttpMethods.DELETE, url)

        RestClient.__check_response(HttpMethods.DELETE, url, response)
        return response.json()

    def __get_request_params(self, data=None):
        headers = {
            'X-Api-Key': self.__api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        if self.__custom_headers is not None:
            for key in self.__custom_headers:
                headers[key] = self.__custom_headers[key]

        model = data.to_model() if (data is not None) else None
        return model, headers

    @staticmethod
    def __check_response(verb, url, response):
        status_code = response.status_code
        if status_code < 200 or status_code > 299:
            try:
                response_body = response.json()
                if status_code == 422 and response_body.get('code', None) is not None:
                    if response.get('code', None) == 'OrderLocked':
                        error = OrderLockedError(response.get('message', None), verb, url)
                    else:
                        error = AmpliaError(verb, url, response.get('code', None), response.get('message', None))
                else:
                    error = RestError(verb, url, status_code, response.get('message', None))

            except Exception:
                error = RestError(verb, url, status_code)

            raise error
        pass

    @property
    def endpoint(self):
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, value):
        self.__endpoint = value

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, value):
        self.__api_key = value

    @property
    def custom_headers(self):
        return self.__custom_headers

    @custom_headers.setter
    def custom_headers(self, value):
        self.__custom_headers = value


__all__ = [
    'RestClient'
]
