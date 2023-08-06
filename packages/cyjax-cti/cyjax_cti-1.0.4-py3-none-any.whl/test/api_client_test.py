import pytest
import requests
import responses
from unittest.mock import patch, Mock

import cyjax
from cyjax import ResponseErrorException, ApiKeyNotFoundException
from cyjax.api_client import ApiClient
from cyjax.exceptions import UnauthorizedException


class TestApiClient:

    def test_api_key_is_not_set(self):
        api_client = ApiClient()
        with pytest.raises(ApiKeyNotFoundException) as exception:
            api_client.send(method='get', endpoint='test/endpoint')

    def test_set_api_key_on_module(self):
        cyjax.api_key = 'module_api_key'
        api_client = ApiClient()
        assert api_client.get_api_key() == 'module_api_key'

    def test_set_api_key_on_constructor(self):
        api_client = ApiClient(api_key='constructor_api_key')
        assert api_client.get_api_key() == 'constructor_api_key'

    def test_set_api_key_on_constructor_has_preferences_over_module(self):
        cyjax.api_key = 'module_api_key'
        api_client = ApiClient(api_key='constructor_api_key')
        assert api_client.get_api_key() == 'constructor_api_key'

    def test_default_proxy_settings(self):
        api_client = ApiClient()
        assert api_client._get_proxies() is None

    def test_set_proxy_settings_on_module(self):
        test_proxies = {'http': 'http://user:pass@10.10.1.0:3333',
                        'https': 'https://user:pass@10.10.1.0:3333'}
        cyjax.proxy_settings = test_proxies
        api_client = ApiClient()
        proxies = api_client._get_proxies()
        assert proxies is not None
        assert test_proxies == proxies

        cyjax.proxy_settings = None

    def test_default_api_url(self):
        assert 'https://api.cyberportal.co' == ApiClient.BASE_URI
        api_clinet = ApiClient(api_key='constructor_api_key')
        assert 'https://api.cyberportal.co' == api_clinet.get_api_url()

    def test_set_api_url_on_module(self):
        cyjax.api_url = 'https://api.module-api-url.com'
        api_client = ApiClient()
        assert api_client.get_api_url() == 'https://api.module-api-url.com'
        cyjax.api_url = None  # Reset to default

    def test_set_api_url_on_client_constructor(self):
        api_clinet = ApiClient(api_key='constructor_api_key', api_url='https://api.new-url-cyjax.com')
        assert 'https://api.new-url-cyjax.com' == api_clinet.get_api_url()

    def test_set_api_url_on_constructor_has_preferences_over_module(self):
        cyjax.api_url = 'https://api.module-api-url.com'
        api_client = ApiClient(None, api_url='http://api.constructor-api-url.com')
        assert api_client.get_api_url() == 'http://api.constructor-api-url.com'
        cyjax.api_url = None  # Reset to default

    @responses.activate
    def test_send(self,):
        api_client = ApiClient(api_key='foo_api_key')
        api_url = api_client.get_api_url()

        responses.add(responses.GET, api_url + '/test/endpoint?param1=test&param2=foo',
                      json=[{'1': 'a', '2': 'b', '3': [1, 2, 3]}], status=200)

        response = api_client.send(method='get', endpoint='test/endpoint', params={'param1': 'test', 'param2': 'foo'},
                                   data={'foo': 'test'})

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == api_url + '/test/endpoint?param1=test&param2=foo'
        assert responses.calls[0].request.body == "foo=test"
        assert responses.calls[0].response.text == '[{"1": "a", "2": "b", "3": [1, 2, 3]}]'

        assert response.status_code == 200
        assert response.json() == [{'1': 'a', '2': 'b', '3': [1, 2, 3]}]

    @responses.activate
    def test_send_compare_request_params(self, mocker):
        api_client = ApiClient(api_key='foo_api_key')
        responses.add(responses.GET, ApiClient.BASE_URI + '/test/endpoint',
                      json={'success': True}, status=200)
        request_method = mocker.spy(requests.api, 'request')

        response = api_client.send(method='get', endpoint='test/endpoint', params={'param1': 'test', 'param2': 'foo'},
                                   data={'foo': 'test'})

        assert response.status_code == 200
        assert response.json().get('success') is True

        request_method.assert_called_once_with(method='get',
                                               url=ApiClient.BASE_URI + '/test/endpoint',
                                               data={'foo': 'test'},
                                               params={'param1': 'test', 'param2': 'foo'},
                                               headers={'Authorization': 'Bearer foo_api_key'},
                                               proxies=None)

    @responses.activate
    def test_send_with_proxies(self, mocker):
        assert cyjax.proxy_settings is None

        test_proxies = {'http': 'http://user:pass@10.10.1.0:3333',
                        'https': 'https://user:pass@10.10.1.0:3333'}
        cyjax.proxy_settings = test_proxies

        api_client = ApiClient(api_key='foo_api_key')
        responses.add(responses.GET, ApiClient.BASE_URI + '/test/endpoint',
                      json={'success': True}, status=200)
        request_method = mocker.spy(requests.api, 'request')

        # with requests
        response = api_client.send(method='get', endpoint='test/endpoint')

        assert response.status_code == 200
        assert response.json().get('success') is True

        request_method.assert_called_once_with(method='get',
                                               url=ApiClient.BASE_URI + '/test/endpoint',
                                               data={},
                                               params={},
                                               headers={'Authorization': 'Bearer foo_api_key'},
                                               proxies=test_proxies)

        cyjax.proxy_settings = None

    @responses.activate
    def test_rest_request_throw_exception(self):
        api_client = ApiClient(api_key='foo_api_key')

        responses.add(responses.GET, api_client.get_api_url() + '/test/endpoint',
                      json={'name': 'Unauthorized', 'message': 'The access token provided is invalid'},
                      status=401)

        with pytest.raises(UnauthorizedException):
            api_client.send(method='get', endpoint='test/endpoint')
