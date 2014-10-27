#!/usr/bin env python
from tests.unit import AWSMockServiceTestCase
from boto.cloudsearch2.cloudsearchhelper import CloudSearchHelper


SEARCH_SERVICE = "search-demo-userdomain.us-east-1.cloudsearch.amazonaws.com"
FULL_URL = 'http://%s/2013-01-01/search' % SEARCH_SERVICE


class CloudSearchSearchAuthTest(AWSMockServiceTestCase):
    connection_class = CloudSearchHelper

    def test_search_with_auth(self):
        helper = self.service_connection
        helper.search({'q': 'Test'})

        headers = None
        if self.actual_request is not None:
            headers = self.actual_request.headers

        self.assertIsNotNone(headers)
        self.assertIsNotNone(headers.get('Authorization'))
