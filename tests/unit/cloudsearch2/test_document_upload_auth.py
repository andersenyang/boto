#!/usr/bin env python
from tests.unit import AWSMockServiceTestCase
from boto.cloudsearch2.cloudsearchhelper import CloudSearchHelper


DOC_SERVICE = "doc-demo-userdomain.us-east-1.cloudsearch.amazonaws.com"
FULL_URL = "http://%s/2013-01-01/documents/batch" % DOC_SERVICE


class CloudSearchDocumentUploadAuthTest(AWSMockServiceTestCase):
    connection_class = CloudSearchHelper

    def test_upload_document_with_auth(self):
        helper = self.service_connection
        helper.upload("1234", {"id": "1234", "title": "Title 1",
                      "category": ["cat_a", "cat_b", "cat_c"]})

        headers = None
        if self.actual_request is not None:
            headers = self.actual_request.headers

        self.assertIsNotNone(headers)
        self.assertIsNotNone(headers.get('Authorization'))
