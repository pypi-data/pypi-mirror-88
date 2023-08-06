#  CYjAX Limited

import responses

from cyjax.api_client import ApiClient
from cyjax.resource import Resource


class TestResourceService:

    @classmethod
    def setup_class(cls):
        api_client = ApiClient(api_key='foo_api_key')
        cls.api_url = api_client.get_api_url()

    @responses.activate
    def test_paginate(self):

        responses.add(responses.GET, self.api_url + '/test/endpoint?param1=test&param2=foo&page=1&per-page='
                      + str(Resource.DEFAULT_ITEMS_PER_PAGE),
                      json=[{"1": "a"}, {"2": "b"}], status=200,
                      headers={'Link': self.api_url +
                                       '/test/endpoint?param1=test&param2=foo&page=2&per-page=1;rel=next'})

        responses.add(responses.GET, self.api_url + '/test/endpoint?param1=test&param2=foo&page=2&per-page='
                      + str(Resource.DEFAULT_ITEMS_PER_PAGE),
                      json=[{"3": "c"}, {"4": "d"}], status=200)

        resource_service = Resource(api_key='9753b80f76bd4293e8c610b07091a37b')
        for x in resource_service.paginate(endpoint='test/endpoint', params={'param1': 'test', 'param2': 'foo'}):
            continue

        assert len(responses.calls) == 2
        assert responses.calls[0].request.url == self.api_url + \
               '/test/endpoint?param1=test&param2=foo&page=1&per-page=' + str(Resource.DEFAULT_ITEMS_PER_PAGE)
        assert responses.calls[0].response.text == '[{"1": "a"}, {"2": "b"}]'

        assert responses.calls[1].request.url == self.api_url + \
               '/test/endpoint?param1=test&param2=foo&page=2&per-page=' + str(Resource.DEFAULT_ITEMS_PER_PAGE)
        assert responses.calls[1].response.text == '[{"3": "c"}, {"4": "d"}]'

        def test_setting_client():
            resource = Resource()
            assert 'https://api.cyberportal.co' == resource._api_client.get_api_url()
            assert resource._api_client.get_api_key() is None

            resource = Resource('123456', 'https://api.new-address.com')
            assert 'https://api.new-address.com' == resource._api_client.get_api_url()
            assert '123456' == resource._api_client.get_api_key()
