cloudify-nexus-plugin
=====================

Cloudify plugin for the Nexus repository (http://www.sonatype.com/nexus)

This plugin was developed for Cloudify version 3.1 and is a part of the regression testing we’re doing therefore should be used with care. 

What it does
------------

The plugin:

1.  downloads resource from Nexus repository according to given GAV.

Basic how-to
-----------

1.  Import the plugin in blueprint.

2.  Add a node that uses tasks from plugin.

3.  In *inputs* for task deploy or undeploy:
    *   add ip address of nexus server as 'address' parameter,
    *   add 'tempdir' parameter,
    *   create `artifact` section (dictionary),
    *   add ip address to the jboss server as `ip` parameter,
    *   add path to directory where resource to be deployed exists as `home_path` parameter,
    *   add path to directory where resource to be deployed exists as `resource_dir` parameter,
    *   add name of deployed resource as `resource_name` parameter,

    for example:

        create: 
          implementation: nexus.nexus.tasks.download
          inputs:
            address: http://11.0.0.8:8081/nexus
            artifact:
              artifactId: artifact
              repositoryId: repository_id
              groupId: groupId
              extension: war
              version: 1.0
            tempdir: /tmp
            resource_name: artifact.war

### Minimum working example ###

The following is a basic working example:

tosca_definitions_version: cloudify_dsl_1_0
imports:
  - http://www.getcloudify.org/spec/cloudify/3.1rc1/types.yaml
  - http://127.0.0.1:8001/plugin.yaml

node_templates:
  myhost:
    type: cloudify.nodes.Compute
    properties:
      ip: 127.0.0.1
      cloudify_agent:
        user: cloudify_user
        key: /home/cloudify_user/.ssh/id_rsa

  resource_downloader:
    type: cloudify.nodes.Root
    interfaces:
      cloudify.interfaces.lifecycle:
        create: 
          implementation: nexus.nexus.tasks.download
          inputs:
            address: http://127.0.0.1:8081/nexus
            artifact:
              artifactId: jboss-helolworld
              repositoryId: repository_id
              groupId: groupId
              extension: war
              version: 1.0
            tempdir: /tmp
            resource_name: artifact.war
    relationships:
      - type: cloudify.relationships.contained_in
        target: myhost

#### Assumptions for the above example ####

*   Both `plugin.yaml` and `plugin.zip` are served on `localhost:8001`.
*   Nexus server is up and running on 'localhost:8081/nexus`
*   Nexus has already uploaded artifact 
*   User `cloudify_user` exists and can be accessed with
    `my secret password`.


