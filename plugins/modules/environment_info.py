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

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.confluent.cloud.plugins.module_utils.confluent_api import AnsibleConfluent, confluent_argument_spec


"""
def main():
    argument_spec = confluent_argument_spec()

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    confluent = AnsibleConfluent(
        module=module,
        resource_path="/org/v2/environments",
    )

    resources = confluent.query()

    if 'kind' in resources and resources['kind'] == 'EnvironmentList':
        confluent.module.exit_json(changed=False, meta={"ping": "pong"})
    else:
        module.fail_json(
            msg='Ping failure',
            fetch_url_info=resources,
        )
"""

def main():
    module = AnsibleModule(
        argument_spec=dict(
            count=dict(type='int', default=1),
            count_offset=dict(type='int', default=1),
            device_ids=dict(type='list', elements='str'),
            facility=dict(),
            features=dict(type='dict'),
            hostnames=dict(type='list', elements='str', aliases=['name']),
            tags=dict(type='list', elements='str'),
            locked=dict(type='bool', default=False, aliases=['lock']),
            operating_system=dict(),
            plan=dict(),
            state=dict(choices=ALLOWED_STATES, default='present'),
            user_data=dict(default=None),
            wait_for_public_IPv=dict(type='int', choices=[4, 6]),
            wait_timeout=dict(type='int', default=900),
            ipxe_script_url=dict(default=''),
            always_pxe=dict(type='bool', default=False),
        ),
        required_one_of=[('device_ids', 'hostnames',)],
        mutually_exclusive=[
            ('hostnames', 'device_ids'),
            ('count', 'device_ids'),
            ('count_offset', 'device_ids'),
        ]
    )

    if not HAS_METAL_SDK:
        module.fail_json(msg='packet-python required for this module')

    state = module.params.get('state')

    try:
        module.exit_json(**act_on_devices(module, state))
    except Exception as e:
        module.fail_json(msg='failed to set device state %s, error: %s' %
                         (state, to_native(e)), exception=traceback.format_exc())

if __name__ == "__main__":
    main()
