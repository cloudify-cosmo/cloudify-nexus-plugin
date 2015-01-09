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
import shutil
import httplib
from cloudify import ctx
from cloudify.decorators import operation
from nexus import nexuscon


@operation
def download(artifact,
             address,
             tempdir,
             resource_name,
             **kwargs):
    """
    Download file
    :param artifact: GAV dictionary
    :param address: nexus address
    :param tempdir: temporary directory to store files
    :param resource_name: name of resource to get saved
    :param kwargs:
    :return:
    """
    ctx.logger.info('Starting Nexus download')
    parameters = get_artifact_parameters(artifact)
    ctx.logger.info('Download filename {0}'.format(resource_name))
    nexus = nexuscon.NexusConnector(address)
    if nexus.download_file(parameters, resource_name, tempdir) != httplib.OK:
        ctx.logger.info("Download file has failed. Exiting.")
        return


@operation
def delete(tempdir,
           resource_name,
           **kwargs):
    """
    Delete resource
    :param tempdir: directory to resource name
    :param resource_name: file to be removed
    :param kwargs:
    :return:
    """
    ctx.logger.info('Deleting filename {0}'.format(resource_name))
    temp_path = tempdir + '\'' + resource_name
    if os.path.exists(temp_path):
        shutil.remove(temp_path)
        ctx.logger.info('Filename removed: [{0}]'.format(resource_name))


def get_artifact_parameters(artifact):
    """
    Get GAV parameters
    :param artifact: artifact dictionary
    :return:
    """
    parameters = dict()
    parameters['a'] = artifact.get('artifactId')
    parameters['r'] = artifact.get('repositoryId')
    parameters['p'] = artifact.get('extension')
    parameters['g'] = artifact.get('groupId')
    parameters['v'] = artifact.get('version')
    return parameters


def get_filename(artifact):
    """
    Get filename
    :param artifact: artifact dictionary
    :return:
    """
    return artifact.get('artifactId') + '.' + artifact.get('extension')
