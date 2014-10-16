#!/usr/bin env python

from tests.unit import unittest
from httpretty import HTTPretty

import json

from boto.cloudsearch2.document import DocumentServiceConnection


HOSTNAME = "doc-demo-userdomain.us-east-1.cloudsearch.amazonaws.com"
FULL_URL = "http://%s/2013-01-01/documents/batch" % HOSTNAME

class CloudSearchDocumentUploadAuthTest(unittest.TestCase):

    def setUp(self):
        HTTPretty.enable()
        HTTPretty.register_uri(
            HTTPretty.POST,
            FULL_URL,
            body=json.dumps({'status': 'success',
                             'adds': 1,
                             'deletes': 0,
                             }).encode('utf-8'),
            content_type="application/json")

    def tearDown(self):
        HTTPretty.disable()

    def test_upload_document_with_auth(self):
        document = DocumentServiceConnection(endpoint=HOSTNAME)
        document.add("1234", {"id": "1234", "title": "Title 1",
                              "category": ["cat_a", "cat_b", "cat_c"]})

        document.commit()
        headers = HTTPretty.last_request.headers

        self.assertIsNotNone(headers.get('Authorization'))
