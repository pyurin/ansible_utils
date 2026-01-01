#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Petr Iurin <p.yurin@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ossconf_edit
short_description: Edit OSSEC XML configuration files using XPath
version_added: "1.0.0"
description:
    - This module provides XML editing capabilities for OSSEC configuration files
    - It uses XPath to locate and modify XML elements
    - Supports setting values, attributes, and raw XML replacement
requirements:
    - lxml
    - requests
options:
    path:
        description:
            - Path to the XML file to edit
        required: true
        type: path
    xpath:
        description:
            - XPath expression to locate the element to modify
        required: false
        type: str
    value:
        description:
            - Text value to set for the element
        required: false
        type: str
    attributes:
        description:
            - Dictionary of attributes to set on the element
        required: false
        type: dict
    task_block:
        description:
            - List of operations to apply in sequence
            - Each operation is a dict with xpath, value, attributes, xml_set_raw, and when_xpath_exist
        required: false
        type: list
        elements: dict
    xml_set_raw:
        description:
            - Raw XML string to replace the matched element
        required: false
        type: str
    when_xpath_exist:
        description:
            - Only perform the operation if this XPath exists
        required: false
        type: str
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
# Set a simple value
- name: Set OSSEC server IP
  pyurin.utils.ossconf_edit:
    path: /var/ossec/etc/ossec.conf
    xpath: /ossec_config/client/server/address
    value: "192.168.1.100"

# Set multiple values using task_block
- name: Configure multiple OSSEC settings
  pyurin.utils.ossconf_edit:
    path: /var/ossec/etc/ossec.conf
    task_block:
      - xpath: /ossec_config/client/server/address
        value: "192.168.1.100"
      - xpath: /ossec_config/client/server/port
        value: "1514"

# Set element with attributes
- name: Add localfile with location attribute
  pyurin.utils.ossconf_edit:
    path: /var/ossec/etc/ossec.conf
    xpath: /ossec_config/localfile[@location='journald']/log_format
    value: "journald"

# Replace with raw XML
- name: Add complete localfile block
  pyurin.utils.ossconf_edit:
    path: /var/ossec/etc/ossec.conf
    xpath: /ossec_config/localfile
    xml_set_raw: |
      <localfile>
        <log_format>syslog</log_format>
        <location>/var/log/messages</location>
      </localfile>

# Conditional operation
- name: Set value only if parent exists
  pyurin.utils.ossconf_edit:
    path: /var/ossec/etc/ossec.conf
    xpath: /ossec_config/client/server/port
    value: "1514"
    when_xpath_exist: /ossec_config/client/server
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
    sample: "XML file modified successfully"
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
    sample: "/var/ossec/etc/ossec.conf.12345.backup"
'''

import os
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pyurin.utils.plugins.module_utils.wazuh.ossconf_edit import ossconf_edit

def main():
    module_args = dict(
        path=dict(type='path', required=True),
        xpath=dict(type='str', required=False, default=None),
        value=dict(type='str', required=False, default=None),
        attributes=dict(type='dict', required=False, default=None),
        task_block=dict(type='list', elements='dict', required=False, default=None),
        xml_set_raw=dict(type='str', required=False, default=None),
        when_xpath_exist=dict(type='str', required=False, default=None),
        backup=dict(type='bool', required=False, default=False),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=[
            ['xpath', 'task_block']
        ]
    )

    # Get parameters
    path = module.params['path']
    xpath = module.params['xpath']
    value = module.params['value']
    attributes = module.params['attributes']
    task_block = module.params['task_block']
    xml_set_raw = module.params['xml_set_raw']
    when_xpath_exist = module.params['when_xpath_exist']
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

    # Process XML
    try:
        modified_content = ossconf_edit(
            xml_content=original_content,
            xpath=xpath,
            value=value,
            attributes=attributes,
            task_block=task_block,
            xml_set_raw=xml_set_raw,
            when_xpath_exist=when_xpath_exist
        )
    except Exception as e:
        module.fail_json(msg=f'Failed to process XML: {str(e)}', **result)

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
                result['msg'] = 'XML file modified successfully'
            except Exception as e:
                module.fail_json(msg=f'Failed to write file {path}: {str(e)}', **result)
        else:
            result['msg'] = 'XML file would be modified (check mode)'
    else:
        result['msg'] = 'No changes needed'

    module.exit_json(**result)


if __name__ == '__main__':
    main()
