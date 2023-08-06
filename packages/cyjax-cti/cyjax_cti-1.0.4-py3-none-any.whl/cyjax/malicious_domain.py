from .helpers import DateHelper
from .resource import Resource


class MaliciousDomain(Resource):

    def __init__(self, api_key=None, api_url=None):
        """
        :param api_key: The API key.
        :param api_url: The Cyjax API url.
        """
        super(MaliciousDomain, self).__init__(api_key=api_key, api_url=api_url)

    def list(self, since=None, until=None):
        """
        Returns potential malicious domains.
        :param since: The start date time.
        :type since: (datetime, timedelta, str), optional
        :param until: The end date time.
        :type until:  (datetime, timedelta, str), optional
        :return: The list of potential malicious domains.
        :rtype list
        """

        params = DateHelper.build_date_params(since=since, until=until)
        return self.paginate(endpoint='domain-monitor/potential-malicious-domain', params=params)
