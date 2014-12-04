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

import os
import httplib
import unittest
from cloudify.mocks import MockCloudifyContext
from cloudify.state import current_ctx
from nexus import nexuscon


class TestNexus(unittest.TestCase):
    """
        This is Nexus integration test. Nexus instance should be at
        https://repository.jboss.org/nexus in (repository id) google, 
        (artifact name) visualization-datasource, (version) 1.0.1, 
        (group id) com.google.visualization, (type) pom. 
    """
    def setUp(self):
        ctx = MockCloudifyContext(
            node_id='id',
            node_name='name')
        current_ctx.set(ctx)

    def test_download_file_no_credentials(self):
        parameters = {"r": "google",
                      "a": "visualization-datasource",
                      "v": "1.0.1",
                      "g": "com.google.visualization",
                      "p": "pom"}
        file_name = 'visualisation-datasource.pom'
        tempdir = '/tmp'
        address = "https://repository.jboss.org/nexus"
        nexus = nexuscon.NexusConnector(address)
        code = nexus.download_file(parameters,
                                   file_name,
                                   tempdir)
        self.assertTrue(code == httplib.OK)
        self.assertTrue(os.path.exists(tempdir + '/' + file_name))

if __name__ == '__main__':
    unittest.main()
