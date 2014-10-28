# Copyright (c) 2014 Amazon.com, Inc. or its affiliates.  All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

import boto.exception
from boto.compat import urllib
from boto.connection import AWSAuthConnection
from boto.exception import JSONResponseError
from boto.regioninfo import RegionInfo


class InvalidRequestMethodException(Exception):
    """
    Invalid request method for search. Method has to be 'GET' or 'POST'
    """
    pass


class CloudSearchAuthConnection(AWSAuthConnection):
    """
    Send signed requests for searches and batch uploads that layer1 does not support.
    """
    APIVersion = "2013-01-01"
    DefaultRegionName = "us-east-1"
    DefaultRegionEndpoint = "cloudsearch.us-east-1.amazonaws.com"
    ResponseError = JSONResponseError

    def __init__(self, host=None, aws_access_key_id=None, aws_secret_access_key=None, region=None, **kwargs):
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionEndpoint)

        if host is None:
            host = region.endpoint

        self.region = region.name
        super(CloudSearchAuthConnection, self).__init__(host=host, aws_access_key_id=aws_access_key_id,
                                                        aws_secret_access_key=aws_secret_access_key, **kwargs)

    def _required_auth_capability(self):
        return ['hmac-v4']

    def process_search_query_for_post(self, params):
        l = []
        for param in sorted(params):
            value = boto.utils.get_utf8_value(params[param])
            l.append('%s=%s' % (urllib.parse.quote(param, safe='-_.~'),
                                urllib.parse.quote(value, safe='-_.~')))
        return '&'.join(l)

    def search(self, query, api_version=APIVersion, method='GET'):
        if method != 'GET' and method != 'POST':
            raise InvalidRequestMethodException("Invalid method type. Method should be 'GET or 'POST'")

        path = "/%s/search" % api_version
        auth_path = None

        if method == 'GET':
            http_request = self.build_base_http_request(method, path, auth_path, params=query, headers=headers)

            self.auth_service_name = 'cloudsearch'
            self.auth_region_name = self.region
        else:
            query = self.process_search_query_for_post(query)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            http_request = self.build_base_http_request(method, path, auth_path, data=query, headers=headers)
            self.auth_service_name = 'cloudsearch'
            self.auth_region_name = self.region

        response = self._mexe(http_request)
        return response

    def upload(self, data, api_version=APIVersion, headers=None):
        method = 'POST'
        path = "/%s/documents/batch" % api_version
        auth_path = None

        http_request = self.build_base_http_request(method, path, auth_path, headers=headers, data=data)

        self.auth_service_name = 'cloudsearch'
        self.auth_region_name = self.region

        response = self._mexe(http_request)
        return response
