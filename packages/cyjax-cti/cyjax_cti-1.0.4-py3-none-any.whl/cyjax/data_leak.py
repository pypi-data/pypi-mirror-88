from .helpers import DateHelper
from .resource import Resource


class LeakedEmail(Resource):

    def __init__(self, api_key=None, api_url=None):
        """
        :param api_key: The API key
        :param api_url: The API URL.
        """
        super(LeakedEmail, self).__init__(api_key=api_key, api_url=api_url)

    def list(self, query=None, since=None, until=None):
        """
        Returns leaked emails.
        :param query: The search query.
        :type query: str, optional
        :param since: The start date time. time.
        :type since: (datetime, timedelta, str), optional
        :param until: The end date time.
        :type until:  (datetime, timedelta, str), optional
        :return: The list of leaked emails.
        :rtype list
        """

        params = DateHelper.build_date_params(since=since, until=until)
        if query:
            params.update({'query': query})

        return self.paginate(endpoint='data-leak/credentials', params=params)
