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
def deploy(*args, **kwargs):
    ctx.logger.info('Starting Nexus download')
    file_name = get_filename()
    parameters = get_artifact_parameters()
    ctx.logger.info('Download filename {0}'.format(file_name))
    nexus = nexuscon.NexusConnector()
    tempdir = ctx.node.properties['tempdir']
    if nexus.download_file(parameters, file_name, tempdir) != httplib.OK:
        ctx.logger.info("Download file has failed. Exiting.")
        return

@operation
def delete(*args, **kwargs):
    file_name = get_filename()
    tempdir = ctx.node.properties['tempdir']
    ctx.logger.info('Deleting filename {0}'.format(file_name))
    temp_path = tempdir + '\'' + file_name
    if os.path.exists(temp_path):
        shutil.remove(temp_path)
        ctx.logger.info('Filename removed: [{0}]'.format(file_name))


def get_artifact_parameters():
    parameters = dict()
    parameters['a'] = ctx.node.properties['artifact']['artifactId']
    parameters['r'] = ctx.node.properties['artifact']['repositoryId']
    parameters['p'] = ctx.node.properties['artifact']['extension']
    parameters['g'] = ctx.node.properties['artifact']['groupId']
    parameters['v'] = ctx.node.properties['artifact']['version']
    return parameters


def get_filename():
    return ctx.node.properties['artifact']['artifactId'] + \
        '.' + ctx.node.properties['artifact']['extension']