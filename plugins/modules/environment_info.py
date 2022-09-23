#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Keith Resar <kresar@confluent.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: environment_info
short_description: Get information on existing environments
description:
  - Verify connectivity and auth the Confluent Cloud API endpoint
version_added: "0.0.1"
author: "Keith Resar (@keithresar)"
extends_documentation_fragment:
  - confluent.cloud.confluent
options:
  names:
    description: List of environment Names
    type: list
    elements: str
  ids:
    description: List of environment Ids
    type: list
    elements: str
"""

EXAMPLES = """
- name: List all available environments
  confluent.cloud.environment_info:
- name: List environments that match the given Ids
  confluent.cloud.environment_info:
    ids:
      - env-f3a90de
      - env-3887de0
- name: List environments that match the given Names
  confluent.cloud.environment_info:
    names:
      - Test
      - Production
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


def get_environments_info(confluent):
    resources = confluent.query()

    if confluent.module.params.get('ids'):
        environments = filter(lambda d: d.id in confluent.module.params.get('ids'), resources['data'])
    elif confluent.module.params.get('names'):
        environments = filter(lambda d: d.display_name in confluent.module.params.get('names'), resources['data'])
    else:
        environments = resources['data']

    return({e['id']:e for e in environments})


def main():
    argument_spec = confluent_argument_spec()
    argument_spec['ids'] = dict(type='list', elements='str')
    argument_spec['names'] = dict(type='list', elements='str')

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ('ids', 'names')
        ]
    )

    confluent = AnsibleConfluent(
        module=module,
        resource_path="/org/v2/environments",
    )

    try:
        module.exit_json(**get_environments_info(confluent))
    except Exception as e:
        module.fail_json(msg='failed to get environment info, error: %s' %
                         (to_native(e)), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
