#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Keith Resar <kresar@confluent.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: environment
short_description: Manage Confluent Cloud Environments
description:
  - Manage Confluent Cloud Environments
version_added: "0.0.1"
author: "Keith Resar (@keithresar)"
extends_documentation_fragment:
  - confluent.cloud.confluent
options:
  id:
    description: Environment Id
    type: str
  name:
    description: Environment name
    type: str
  state:
    description:
      - If `absent`, the environment and all objects (clusters, service accounts) will be removed.
        Note that absent will not cause Environment to fail if the Environment does not exist.
      - If `present`, the environment will be created.
    default: present
    choices:
      - absent
      - present
    type: str
"""

EXAMPLES = """
- name: Create new environment
  confluent.cloud.environment:
    name: test_env
    state: present
- name: Delete existing environment by name
  confluent.cloud.environment:
    name: test_env
    state: absent
- name: Modify existing environment by Id
  confluent.cloud.environment:
    id: env-dsh38dja
    name: test_env_new
    state: present
"""

RETURN = """
---
confluent_api:
  description: Response from Confluent Coud API with a few additions/modification.
  returned: success
  type: dict
  contains:
    api_timeout:
      description: Timeout used for the API requests.
      returned: success
      type: int
      sample: 60
    api_retries:
      description: Amount of max retries for the API requests.
      returned: success
      type: int
      sample: 5
    api_retry_max_delay:
      description: Exponential backoff delay in seconds between retries up to this max delay value.
      returned: success
      type: int
      sample: 12
    api_endpoint:
      description: Endpoint used for the API requests.
      returned: success
      type: str
      sample: https://api.confluent.cloud
enviroment_info:
  description: Response
  returned: success
  type: dict
  contains:
    status:
      description: Status.
      returned: success
      type: str
      sample: success
"""

import traceback
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.confluent.cloud.plugins.module_utils.confluent_api import AnsibleConfluent, confluent_argument_spec


def environment_remove(module, resource_id):
    confluent = AnsibleConfluent(
        module=module,
        resource_path="/org/v2/environments",
        resource_key_id=resource_id
    )

    return(confluent.absent())


def environment_create(module):
    confluent = AnsibleConfluent(
        module=module,
        resource_path="/org/v2/environments",
    )

    return(confluent.create({'display_name': module.params.get('name')}))


def environment_update(module, environment):
    confluent = AnsibleConfluent(
        module=module,
        resource_path="/org/v2/environments",
        resource_key_id=environment['id']
    )

    return(confluent.update(environment, {
                'display_name': module.params.get('name'),
     }))


def get_environments(module):
    confluent = AnsibleConfluent(
        module=module,
        resource_path="/org/v2/environments",
    )

    resources = confluent.query()
    return(resources['data'])


def environment_process(module):
    # Get existing environment if it exists
    environments = get_environments(module)
    #return({'a':environments})
    if module.params.get('id') and \
     len([e for e in environments if e['id'] in module.params.get('id')]):
        environment = [e for e in environments if e['id'] in module.params.get('id')][0]
    elif module.params.get('name') and \
     len([e for e in environments if e['display_name'] in module.params.get('name')]):
        environment = [e for e in environments if e['display_name'] in module.params.get('name')][0]
    else:
        environment = None

    # Manage environment removal
    if module.params.get('state') == 'absent' and not environment:
        return({"changed": False})
    elif module.params.get('state') == 'absent' and environment:
        return(environment_remove(module, environment['id']))

    # Create environment
    elif module.params.get('state') == 'present' and not environment:
        return(environment_create(module))

    # Check for update
    else:
        return(environment_update(module, environment))

    # TODO - if state: present indicate if it matches
    # TODO -    if no match then change.


def main():
    argument_spec = confluent_argument_spec()
    argument_spec['id'] = dict(type='str')
    argument_spec['name'] = dict(type='str')
    argument_spec['state'] = dict(default='present', choices=['present', 'absent'])

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    try:
        module.exit_json(**environment_process(module))
    except Exception as e:
        module.fail_json(msg='failed to get environment, error: %s' %
                         (to_native(e)), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
