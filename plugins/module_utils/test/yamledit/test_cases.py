#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Test cases for yamledit module"""

test_cases = [
    # Test 1: Set a simple scalar value
    {
        'description': 'Set a simple string value',
        'yaml_from': '''
name: old_value
version: 1.0
''',
        'key': 'name',
        'separator': '.',
        'value': 'new_value',
        'state': 'present',
        'yaml_to': '''
name: new_value
version: 1.0
'''
    },

    # Test 2: Set a nested scalar value
    {
        'description': 'Set a nested value',
        'yaml_from': '''
server:
  host: localhost
  port: 8080
''',
        'key': 'server.host',
        'separator': '.',
        'value': 'example.com',
        'state': 'present',
        'yaml_to': '''
server:
  host: example.com
  port: 8080
'''
    },

    # Test 3: Create new nested structure
    {
        'description': 'Create new nested structure',
        'yaml_from': '''
name: test
''',
        'key': 'server.database.host',
        'separator': '.',
        'value': 'db.example.com',
        'state': 'present',
        'yaml_to': '''
name: test
server:
  database:
    host: db.example.com
'''
    },

    # Test 4: Set a list value
    {
        'description': 'Set a list value',
        'yaml_from': '''
name: test
''',
        'key': 'allowed_hosts',
        'separator': '.',
        'value': ['localhost', '127.0.0.1', 'example.com'],
        'state': 'present',
        'yaml_to': '''
name: test
allowed_hosts:
- localhost
- 127.0.0.1
- example.com
'''
    },

    # Test 5: Set a dict value
    {
        'description': 'Set a dict value',
        'yaml_from': '''
name: test
''',
        'key': 'database',
        'separator': '.',
        'value': {'host': 'localhost', 'port': 5432, 'name': 'mydb'},
        'state': 'present',
        'yaml_to': '''
name: test
database:
  host: localhost
  port: 5432
  name: mydb
'''
    },

    # Test 6: Set a value in a list by index
    {
        'description': 'Set a value in a list by index',
        'yaml_from': '''
servers:
  - name: server1
    ip: 192.168.1.1
  - name: server2
    ip: 192.168.1.2
''',
        'key': 'servers.0.name',
        'separator': '.',
        'value': 'primary-server',
        'state': 'present',
        'yaml_to': '''
servers:
- name: primary-server
  ip: 192.168.1.1
- name: server2
  ip: 192.168.1.2
'''
    },

    # Test 7: Remove a key (state=absent)
    {
        'description': 'Remove a key',
        'yaml_from': '''
name: test
debug: true
version: 1.0
''',
        'key': 'debug',
        'separator': '.',
        'value': None,
        'state': 'absent',
        'yaml_to': '''
name: test
version: 1.0
'''
    },

    # Test 8: Remove a nested key
    {
        'description': 'Remove a nested key',
        'yaml_from': '''
server:
  host: localhost
  port: 8080
  debug: true
''',
        'key': 'server.debug',
        'separator': '.',
        'value': None,
        'state': 'absent',
        'yaml_to': '''
server:
  host: localhost
  port: 8080
'''
    },

    # Test 9: Use custom separator
    {
        'description': 'Use custom separator',
        'yaml_from': '''
name: test
''',
        'key': 'server/host/ip',
        'separator': '/',
        'value': '192.168.1.100',
        'state': 'present',
        'yaml_to': '''
name: test
server:
  host:
    ip: 192.168.1.100
'''
    },

    # Test 10: Set numeric value
    {
        'description': 'Set numeric value',
        'yaml_from': '''
name: test
''',
        'key': 'port',
        'separator': '.',
        'value': 8080,
        'state': 'present',
        'yaml_to': '''
name: test
port: 8080
'''
    },

    # Test 11: Set boolean value
    {
        'description': 'Set boolean value',
        'yaml_from': '''
name: test
''',
        'key': 'enabled',
        'separator': '.',
        'value': True,
        'state': 'present',
        'yaml_to': '''
name: test
enabled: true
'''
    },

    # Test 12: Remove non-existent key (should not change anything)
    {
        'description': 'Remove non-existent key',
        'yaml_from': '''
name: test
version: 1.0
''',
        'key': 'nonexistent',
        'separator': '.',
        'value': None,
        'state': 'absent',
        'yaml_to': '''
name: test
version: 1.0
'''
    },

    # Test 13: Set value in empty YAML
    {
        'description': 'Set value in empty YAML',
        'yaml_from': '',
        'key': 'name',
        'separator': '.',
        'value': 'test',
        'state': 'present',
        'yaml_to': '''
name: test
'''
    },

    # Test 14: Update existing list element
    {
        'description': 'Update existing list element',
        'yaml_from': '''
items:
  - apple
  - banana
  - cherry
''',
        'key': 'items.1',
        'separator': '.',
        'value': 'blueberry',
        'state': 'present',
        'yaml_to': '''
items:
- apple
- blueberry
- cherry
'''
    },

    # Test 15: Remove list element by index
    {
        'description': 'Remove list element by index',
        'yaml_from': '''
items:
  - apple
  - banana
  - cherry
''',
        'key': 'items.1',
        'separator': '.',
        'value': None,
        'state': 'absent',
        'yaml_to': '''
items:
- apple
- cherry
'''
    },

    # Test 16: Append unique to non-existent key (creates list)
    {
        'description': 'Append unique to non-existent key',
        'yaml_from': '''
name: test
''',
        'key': 'packages',
        'separator': '.',
        'value': 'nginx',
        'state': 'present',
        'append_unique': True,
        'yaml_to': '''
name: test
packages:
- nginx
'''
    },

    # Test 17: Append unique to existing list (value not present)
    {
        'description': 'Append unique to existing list (value not present)',
        'yaml_from': '''
packages:
  - nginx
  - redis
''',
        'key': 'packages',
        'separator': '.',
        'value': 'postgresql',
        'state': 'present',
        'append_unique': True,
        'yaml_to': '''
packages:
- nginx
- redis
- postgresql
'''
    },

    # Test 18: Append unique to existing list (value already present)
    {
        'description': 'Append unique to existing list (value already present)',
        'yaml_from': '''
packages:
  - nginx
  - redis
  - postgresql
''',
        'key': 'packages',
        'separator': '.',
        'value': 'redis',
        'state': 'present',
        'append_unique': True,
        'yaml_to': '''
packages:
- nginx
- redis
- postgresql
'''
    },

    # Test 19: Append unique to nested key
    {
        'description': 'Append unique to nested key',
        'yaml_from': '''
server:
  name: myserver
''',
        'key': 'server.allowed_hosts',
        'separator': '.',
        'value': 'example.com',
        'state': 'present',
        'append_unique': True,
        'yaml_to': '''
server:
  name: myserver
  allowed_hosts:
  - example.com
'''
    },

    # Test 20: Append unique with multiple values sequentially
    {
        'description': 'Append unique - second append',
        'yaml_from': '''
packages:
- nginx
''',
        'key': 'packages',
        'separator': '.',
        'value': 'redis',
        'state': 'present',
        'append_unique': True,
        'yaml_to': '''
packages:
- nginx
- redis
'''
    },
]
