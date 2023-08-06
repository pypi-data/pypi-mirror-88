from json.decoder import JSONDecodeError

import requests

import cyjax
from .exceptions import ResponseErrorException, ApiKeyNotFoundException, UnauthorizedException, TooManyRequestsException


class ApiClient(object):
    """
    The Cyjax REST API URL.
    """
    BASE_URI = 'https://api.cyberportal.co'

    def __init__(self, api_key=None, api_url=None):
        """
        :param api_key: The API key.
        :param api_url: The API URL. If not set uses the default API URL.
        """
        self.__api_key = api_key if api_key else cyjax.api_key
        self.__api_url = api_url if api_url is not None else \
            cyjax.api_url if cyjax.api_url is not None else ApiClient.BASE_URI
        self.__proxies = cyjax.proxy_settings

    def send(self, method, endpoint, params=None, data=None):
        """
        Send a request to an endpoint.
        :param method: The request method: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``
        :type method: str
        :param endpoint: The endpoint.
        :type endpoint: str
        :param params: The list of tuples or bytes to send in the query string for the request
        :type params:  Dictionary, optional
        :param data: The list of tuples, bytes, or file-like object to send in the body of the request
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        :raises ResponseErrorException: Whether the request fails.
        :raises ApiKeyNotFoundException: Whether the API key is not provided.
        :raises UnauthorizedException: Whether the API key is not authorized to perform the request.
        :raises TooManyRequestsException: Whether the API key exceeds the rate limit.
        """

        if data is None:
            data = {}
        if params is None:
            params = {}
        if not self.__api_key:
            raise ApiKeyNotFoundException()

        url = self.get_api_url() + '/' + endpoint
        response = requests.api.request(method=method,
                                        url=url,
                                        params=params,
                                        data=data,
                                        headers={'Authorization': 'Bearer ' + self.__api_key},
                                        proxies=self._get_proxies())

        if response.status_code == 401:
            raise UnauthorizedException()
        elif response.status_code == 429:
            raise TooManyRequestsException()
        elif response.status_code != 200:
            try:
                json_data = response.json()
                raise ResponseErrorException(response.status_code,
                                             json_data['message'] if 'message' in json_data else 'Unknown')
            except JSONDecodeError:
                raise ResponseErrorException(response.status_code, 'Error parsing response %s' % response.text)

        return response

    def get_api_key(self):
        """
        Get API key.
        :return: The API key.
        :rtype: str
        """
        return self.__api_key

    def _get_proxies(self):
        """
        Get the proxies dictionary with proxy settings.
        :return: The proxies dictionary.
        :rtype: dict|None
        """
        if isinstance(self.__proxies, dict):
            return self.__proxies

        return None

    def get_api_url(self):
        """
                Get the API url.
                :return: The API url.
                :rtype: str
                """
        return self.__api_url
