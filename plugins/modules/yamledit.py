#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Petr Iurin <p.yurin@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: yamledit
short_description: Edit YAML files by setting or removing values
version_added: "1.0.0"
description:
    - This module provides YAML editing capabilities
    - It uses a separator-delimited path to locate and modify YAML elements
    - Supports setting scalar, list, and dict values
    - Supports removing elements with state=absent
requirements:
    - yaml
notes:
    - The file must exist before editing
options:
    path:
        description:
            - Path to the YAML file to edit
        required: true
        type: path
    key:
        description:
            - Path to the element in YAML file, separated by separator
            - For nested structures, use the separator to navigate (e.g., 'server.host.ip')
            - For list indices, use numbers (e.g., 'servers.0.name')
        required: true
        type: str
    separator:
        description:
            - Separator used in the key path
        required: false
        type: str
        default: "."
    value:
        description:
            - Value to set at the key path
            - Can be a scalar (string, number, boolean), list, or dict
            - Ignored when state=absent
        required: false
        type: raw
    state:
        description:
            - Whether to set (present) or remove (absent) the element
        required: false
        type: str
        choices: ['present', 'absent']
        default: 'present'
    append_unique:
        description:
            - If true, append value to a list only if it doesn't already exist
            - If the key doesn't exist, an empty list will be created
            - If the key exists but is not a list, an error will be raised
            - Cannot be used with state=absent or with list indices
        required: false
        type: bool
        default: false
    backup:
        description:
            - Create a backup file before modifying
        required: false
        type: bool
        default: false
author:
    - Your Name (@yourhandle)
'''

EXAMPLES = r'''
# Set a simple string value
- name: Set server hostname
  pyurin.utils.yamledit:
    path: /etc/config.yml
    key: server.hostname
    value: "example.com"

# Set a number value
- name: Set server port
  pyurin.utils.yamledit:
    path: /etc/config.yml
    key: server.port
    value: 8080

# Set a list value
- name: Set allowed hosts
  pyurin.utils.yamledit:
    path: /etc/config.yml
    key: server.allowed_hosts
    value:
      - "localhost"
      - "127.0.0.1"
      - "example.com"

# Set a dict value
- name: Set database config
  pyurin.utils.yamledit:
    path: /etc/config.yml
    key: database
    value:
      host: "localhost"
      port: 5432
      name: "mydb"

# Set a value in a list by index
- name: Update first server name
  pyurin.utils.yamledit:
    path: /etc/config.yml
    key: servers.0.name
    value: "primary-server"

# Remove a key
- name: Remove debug setting
  pyurin.utils.yamledit:
    path: /etc/config.yml
    key: debug
    state: absent

# Use custom separator
- name: Set value with slash separator
  pyurin.utils.yamledit:
    path: /etc/config.yml
    key: server/host/ip
    separator: "/"
    value: "192.168.1.100"

# Append unique value to a list
- name: Add host to allowed_hosts if not present
  pyurin.utils.yamledit:
    path: /etc/config.yml
    key: allowed_hosts
    value: "new-host.example.com"
    append_unique: true

# Append unique value (creates list if key doesn't exist)
- name: Add package to dependencies
  pyurin.utils.yamledit:
    path: /etc/config.yml
    key: packages
    value: "nginx"
    append_unique: true

# Create backup before editing
- name: Set value with backup
  pyurin.utils.yamledit:
    path: /etc/config.yml
    key: server.hostname
    value: "new-hostname.com"
    backup: true
'''

RETURN = r'''
changed:
    description: Whether the file was modified
    type: bool
    returned: always
    sample: true
msg:
    description: Human readable message about what happened
    type: str
    returned: always
    sample: "YAML file modified successfully"
diff:
    description: Differences between original and modified content
    type: dict
    returned: when changed
    contains:
        before:
            description: Content before modification
            type: str
        after:
            description: Content after modification
            type: str
backup_file:
    description: Path to the backup file if created
    type: str
    returned: when backup=true and changed
    sample: "/etc/config.yml.12345.backup"
'''

import os
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pyurin.utils.plugins.module_utils.yamledit import yamledit

def main():
    module_args = dict(
        path=dict(type='path', required=True),
        key=dict(type='str', required=True),
        separator=dict(type='str', required=False, default='.'),
        value=dict(type='raw', required=False, default=None),
        state=dict(type='str', required=False, default='present', choices=['present', 'absent']),
        append_unique=dict(type='bool', required=False, default=False),
        backup=dict(type='bool', required=False, default=False),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    # Get parameters
    path = module.params['path']
    key = module.params['key']
    separator = module.params['separator']
    value = module.params['value']
    state = module.params['state']
    append_unique = module.params['append_unique']
    backup = module.params['backup']

    # Check if file exists
    if not os.path.exists(path):
        module.fail_json(msg=f'File {path} does not exist', **result)

    # Read original content
    try:
        with open(path, 'r') as f:
            original_content = f.read()
    except Exception as e:
        module.fail_json(msg=f'Failed to read file {path}: {str(e)}', **result)

    # Process YAML
    try:
        modified_content = yamledit(
            yaml_content=original_content,
            key=key,
            separator=separator,
            value=value,
            state=state,
            append_unique=append_unique
        )
    except Exception as e:
        module.fail_json(msg=f'Failed to process YAML: {str(e)}', **result)

    # Check if content changed
    if original_content != modified_content:
        result['changed'] = True
        result['diff'] = {
            'before': original_content,
            'after': modified_content
        }

        # If not in check mode, write the file
        if not module.check_mode:
            # Create backup if requested
            if backup:
                backup_file = module.backup_local(path)
                result['backup_file'] = backup_file

            # Write modified content
            try:
                with open(path, 'w') as f:
                    f.write(modified_content)
                result['msg'] = 'YAML file modified successfully'
            except Exception as e:
                module.fail_json(msg=f'Failed to write file {path}: {str(e)}', **result)
        else:
            result['msg'] = 'YAML file would be modified (check mode)'
    else:
        result['msg'] = 'No changes needed'

    module.exit_json(**result)


if __name__ == '__main__':
    main()
