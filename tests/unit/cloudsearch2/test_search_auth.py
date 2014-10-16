#!/usr/bin env python

from tests.unit import unittest
from httpretty import HTTPretty

import json

from boto.cloudsearch2.search import SearchConnection


HOSTNAME = "search-demo-userdomain.us-east-1.cloudsearch.amazonaws.com"
FULL_URL = 'http://%s/2013-01-01/search' % HOSTNAME

class CloudSearchSearchAuthTest(unittest.TestCase):

    response = {
        'rank': '-text_relevance',
        'match-expr': "Test",
        'hits': {
            'found': 30,
            'start': 0,
            'hit': [
                {
                    'id': '12341',
                    'fields': {
                        'title': 'Document 1',
                        'rank': 1
                    }
                }
            ]
        },
        'status': {
            'rid': 'b7c167f6c2da6d93531b9a7b314ad030b3a74803b4b7797edb905ba5a6a08',
            'time-ms': 2,
            'cpu-time-ms': 0
        }
    }

    def setUp(self):
        HTTPretty.enable()
        body = self.response
        if not isinstance(body, bytes):
            body = json.dumps(body).encode('utf-8')

        HTTPretty.register_uri(
            HTTPretty.GET,
            FULL_URL,
            body=body,
            content_type="application/json",
            status=200)

    def tearDown(self):
        HTTPretty.disable()

    def test_search_with_auth(self):
        search = SearchConnection(endpoint=HOSTNAME)

        search.search(q='Test', options='TestOptions')
        headers = HTTPretty.last_request.headers

        self.assertIsNotNone(headers.get('Authorization'))
