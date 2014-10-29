#!/usr/bin env python
from tests.unit import AWSMockServiceTestCase
from boto.cloudsearch2.cloudsearchauthconnection import CloudSearchAuthConnection


class CloudSearchAuthConnectionTest(AWSMockServiceTestCase):
    connection_class = CloudSearchAuthConnection

    def test_build_query_string(self):
        helper = self.service_connection

        params = {}
        query = helper.build_query_string(params)
        self.assertEqual(query, '')

        params = {'test': u'test string'}
        query = helper.build_query_string(params)
        self.assertEqual(query, 'test=test%20string')

        params = {'test': b'test string'}
        query = helper.build_query_string(params)
        self.assertEqual(query, 'test=test%20string')

        params = None
        query = helper.build_query_string(params)
        self.assertEqual(query, '')

    def test_upload_document_with_auth(self):
        helper = self.service_connection
        helper.upload("1234", {"id": "1234", "title": "Title 1",
                      "category": ["cat_a", "cat_b", "cat_c"]})

        headers = None
        if self.actual_request is not None:
            headers = self.actual_request.headers

        self.assertIsNotNone(headers)
        self.assertIsNotNone(headers.get('Authorization'))

    def test_search_with_auth(self):
        helper = self.service_connection
        helper.search({'q': 'Test'})

        headers = None
        if self.actual_request is not None:
            headers = self.actual_request.headers

        self.assertIsNotNone(headers)
        self.assertIsNotNone(headers.get('Authorization'))