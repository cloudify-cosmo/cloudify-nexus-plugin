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

import httplib
from cloudify import ctx
from cloudify.decorators import operation
from nexus import nexuscon

@operation
def download(artifact, address, tempdir, **kwargs):
    ctx.logger.info('Starting Nexus download')
    file_name = 'dummy.war'
    parameters = get_artifact_parameters(artifact)
    ctx.logger.info('Download filename {0}'.format(file_name))
    nexus = nexuscon.NexusConnector(address)
    if nexus.download_file(parameters, file_name, tempdir) != httplib.OK:
        ctx.logger.info("Download file has failed. Exiting.")
        return

@operation
def delete(tempdir, **kwargs):
    file_name = 'dummy.war'
    ctx.logger.info('Deleting filename {0}'.format(file_name))
    temp_path = tempdir + '\'' + file_name
    if os.path.exists(temp_path):
        shutil.remove(temp_path)
        ctx.logger.info('Filename removed: [{0}]'.format(file_name))


def get_artifact_parameters(artifact):
    parameters = dict()
    parameters['a'] = artifact.get('artifactId')
    parameters['r'] = artifact.get('repositoryId')
    parameters['p'] = artifact.get('extension')
    parameters['g'] = artifact.get('groupId')
    parameters['v'] = artifact.get('version')
    return parameters


def get_filename(artifact):
    return artifact.get('artifactId') + '.' + artifact.get('extension')