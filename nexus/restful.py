###############################################################################
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
###############################################################################

import urllib2
from cloudify import ctx
import base64


class RestRequest:
    @staticmethod
    def make_request(url, data, method):
        """
        Creates urllib2.Request.
        :param url: request url
        :param data: request data
        :param method: request method
        :return:
        """
        request = urllib2.Request(url, data=data)
        request.get_method = lambda: method
        return request

    @staticmethod
    def add_authentication(user, password, request):
        """
        Add basic HTTP authentication.
        :param user: user name
        :param password: user password
        :param request: request created by create_request
        :return:
        """
        if user is None or password is None:
            return request
        base64string = base64\
            .encodestring('%s:%s' % (user, password))\
            .replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        return request

    @staticmethod
    def prepare_request(url, method, user=None, password=None, data=None):
        """
        Prepare request with given parameters, credentials and data.
        :param url: request url
        :param method: request method
        :param user: user name
        :param password: user password
        :param data: user data
        :return:
        """
        request = RestRequest.make_request(url, data, method)
        request = RestRequest.add_authentication(user, password, request)
        return request

    @staticmethod
    def process_request(request):
        """
        Send prepared request and log errors if occur
        :param request: prepared request by prepare_request()
        :return: url: request url
        :return code: error code
        """
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        code = None
        url = None
        try:
            url = opener.open(request)
            code = url.getcode()
        except urllib2.HTTPError as e:
            code = e.code
            ctx.logger.error('Error code: {0} Reason: {1}'
                             .format(e.code, e.reason))
        finally:
            return url, code
