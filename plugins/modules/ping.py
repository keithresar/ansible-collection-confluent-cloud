#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Keith Resar <kresar@confluent.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: ping
short_description: Verify module connectivity
description:
  - Verify connectivity and auth the Confluent Cloud API endpoint
version_added: "0.0.1"
author: "Keith Resar (@keithresar)"
extends_documentation_fragment:
  - confluent.cloud.confluent
"""

EXAMPLES = """
- name: Verify connectivity
  confluent.cloud.ping:
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
ping:
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


if __name__ == "__main__":
    main()
