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
    options:
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
from environments_info import get_environments_info


def environment_present(module):
"""
def get_environments_info(confluent):
    resources = confluent.query()

    if confluent.module.params.get('ids'):
        environments = [e for e in resources['data'] if e['id'] in confluent.module.params.get('ids')]
    elif confluent.module.params.get('names'):
        environments = [e for e in resources['data'] if e['display_name'] in confluent.module.params.get('names')]
    else:
        environments = resources['data']

    return({e['id']: e for e in environments})
"""

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
        module.exit_json(**get_environments_info(confluent))
    except Exception as e:
        module.fail_json(msg='failed to get environment, error: %s' %
                         (to_native(e)), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
