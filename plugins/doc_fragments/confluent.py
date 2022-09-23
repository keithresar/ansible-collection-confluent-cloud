# Copyright: (c) 2022, 
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    # Standard documentation
    DOCUMENTATION = r'''
    options:
        api_key:
            description:
                - Confluent Cloud API Key
            type: str
            required: true
        api_secret:
            description:
                - Confluent Cloud API Secret
            type: str
            required: true
    '''
