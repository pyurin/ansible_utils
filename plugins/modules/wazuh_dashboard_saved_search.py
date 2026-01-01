#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Petr Iurin <p.yurin@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: wazuh_dashboard_saved_search
short_description: Create or update a saved search in Wazuh Dashboard
version_added: "1.0.0"
description:
    - This module creates or updates a saved search in OpenSearch Dashboards (Wazuh Dashboard)
    - It uses the OpenSearch API to manage saved search objects
    - Automatically detects if a saved search with the same title exists and updates it
options:
    dashboard_host:
        description:
            - Hostname or IP address of the Wazuh Dashboard
        required: true
        type: str
    username:
        description:
            - Username for authenticating to the Wazuh Dashboard
        required: true
        type: str
    password:
        description:
            - Password for authenticating to the Wazuh Dashboard
        required: true
        type: str
        no_log: true
    saved_search_title:
        description:
            - Title for the saved search
            - Used as the display name and for identifying existing searches
        required: true
        type: str
    filter:
        description:
            - Filter string in simple format
            - Example C(agent.name:Mac-mini.local and not rule.groups:auth_failed)
            - Multiple conditions can be combined with 'and'
            - Use 'not' prefix to negate a condition
        required: false
        type: str
    columns:
        description:
            - List of column names to display in the saved search
            - Default is ["timestamp", "agent.name", "rule.description", "rule.level", "rule.id"]
        required: false
        type: list
        elements: str
    description:
        description:
            - Description for the saved search
            - If not provided, uses the saved_search_title
        required: false
        type: str
    port:
        description:
            - Port number for the Wazuh Dashboard
        required: false
        type: int
        default: 443
author:
    - Your Name (@yourhandle)
'''

EXAMPLES = r'''
# Create a simple saved search
- name: Create saved search for Mac mini agent
  pyurin.utils.wazuh_dashboard_saved_search:
    dashboard_host: "192.168.1.100"
    username: "admin"
    password: "SecretPassword123"
    saved_search_title: "Mac mini Logs"
    filter: "agent.name:Mac-mini.local"

# Create saved search with custom columns
- name: Create saved search with authentication failures
  pyurin.utils.wazuh_dashboard_saved_search:
    dashboard_host: "wazuh-dashboard.example.com"
    username: "admin"
    password: "SecretPassword123"
    saved_search_title: "Authentication Failures"
    filter: "rule.groups:authentication_failed"
    columns:
      - "timestamp"
      - "agent.name"
      - "rule.description"
      - "data.srcip"
      - "data.srcuser"
    description: "All authentication failure events"

# Create saved search with complex filter
- name: Create saved search excluding auth failures for specific agent
  pyurin.utils.wazuh_dashboard_saved_search:
    dashboard_host: "192.168.1.100"
    username: "admin"
    password: "SecretPassword123"
    saved_search_title: "Mac mini (no auth failures)"
    filter: "agent.name:Mac-mini.local and not rule.groups:auth_failed"
    description: "Mac mini logs excluding authentication failures"

# Create saved search on custom port
- name: Create saved search on non-standard port
  pyurin.utils.wazuh_dashboard_saved_search:
    dashboard_host: "192.168.1.100"
    username: "admin"
    password: "SecretPassword123"
    saved_search_title: "Custom Search"
    filter: "rule.level:10"
    port: 8443
'''

RETURN = r'''
changed:
    description: Whether the saved search was created or updated
    type: bool
    returned: always
    sample: true
msg:
    description: Human readable message about what happened
    type: str
    returned: always
    sample: "Saved search created successfully"
saved_search_id:
    description: ID of the created or updated saved search
    type: str
    returned: when successful
    sample: "abc123-def456-ghi789"
saved_search_title:
    description: Title of the saved search
    type: str
    returned: when successful
    sample: "Mac mini Logs"
'''

import requests
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pyurin.utils.plugins.module_utils.wazuh.dashboard.create_saved_search import create_saved_search

def run_module():

    module_args = dict(
        dashboard_host=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        saved_search_title=dict(type='str', required=True),
        filter=dict(type='str', required=False, default=None),
        columns=dict(type='list', elements='str', required=False, default=None),
        description=dict(type='str', required=False, default=None),
        port=dict(type='int', required=False, default=443),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,  # API operations cannot be simulated in check mode
    )


    # Get parameters
    dashboard_host = module.params['dashboard_host']
    username = module.params['username']
    password = module.params['password']
    saved_search_title = module.params['saved_search_title']
    filter_str = module.params['filter']
    columns = module.params['columns']
    description = module.params['description']
    port = module.params['port']

    # Call the create_saved_search function
    try:
        # Import the API functions to check if search already exists
        from ansible_collections.pyurin.utils.plugins.module_utils.wazuh.dashboard.api import (
            find_saved_objects
        )

        # Check if saved search already exists
        find_success, existing_objects, find_error = find_saved_objects(
            dashboard_host=dashboard_host,
            object_type='search',
            search_term=saved_search_title,
            username=username,
            password=password,
            port=port
        )

        existing_object_id = None
        if find_success and existing_objects:
            # Filter to exact title match
            exact_matches = [obj for obj in existing_objects
                           if obj.get('attributes', {}).get('title') == saved_search_title]

            if exact_matches:
                existing_object_id = exact_matches[0].get('id')

        # Create or update the saved search
        create_saved_search(
            dashboard_host=dashboard_host,
            username=username,
            password=password,
            saved_search_title=saved_search_title,
            filter=filter_str,
            columns=columns,
            description=description,
            port=port
        )

        # Get the saved search ID after creation/update
        find_success, objects_after, _ = find_saved_objects(
            dashboard_host=dashboard_host,
            object_type='search',
            search_term=saved_search_title,
            username=username,
            password=password,
            port=port
        )

        saved_search_id = None
        if find_success and objects_after:
            exact_matches = [obj for obj in objects_after
                           if obj.get('attributes', {}).get('title') == saved_search_title]
            if exact_matches:
                saved_search_id = exact_matches[0].get('id')

        # Determine if this was an update or create
        if existing_object_id:
            result['msg'] = f'Saved search "{saved_search_title}" updated successfully'
        else:
            result['msg'] = f'Saved search "{saved_search_title}" created successfully'

        result['changed'] = True
        result['saved_search_title'] = saved_search_title
        if saved_search_id:
            result['saved_search_id'] = saved_search_id

    except Exception as e:
        module.fail_json(
            msg=f'Failed to create/update saved search: {str(e)}',
            **result
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
