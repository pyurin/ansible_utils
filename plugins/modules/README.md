# Pyurin Utils Ansible Modules

This directory contains Ansible modules for the `pyurin.utils` collection.

## Available Modules

### wazuh_dashboard_saved_search

Creates or updates a saved search in Wazuh Dashboard (OpenSearch Dashboards).

**Requirements:**
- Python `requests` library
- Access to Wazuh Dashboard API

**Parameters:**

| Parameter | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| dashboard_host | yes | str | - | Hostname or IP of Wazuh Dashboard |
| username | yes | str | - | Dashboard username |
| password | yes | str | - | Dashboard password |
| saved_search_title | yes | str | - | Title for the saved search |
| filter | no | str | None | Filter string (e.g., 'agent.name:host and not rule.groups:auth') |
| columns | no | list | ["timestamp", "agent.name", "rule.description", "rule.level", "rule.id"] | Columns to display |
| description | no | str | saved_search_title | Description for the saved search |
| port | no | int | 443 | Dashboard port number |

**Example:**

```yaml
- name: Create saved search for specific agent
  pyurin.utils.wazuh_dashboard_saved_search:
    dashboard_host: "192.168.1.100"
    username: "admin"
    password: "SecretPassword123"
    saved_search_title: "Mac mini Logs"
    filter: "agent.name:Mac-mini.local and not rule.groups:auth_failed"
    columns:
      - "timestamp"
      - "agent.name"
      - "rule.description"
      - "rule.level"
```

### ossconf_edit

Edits OSSEC/Wazuh XML configuration files using XPath.

**Requirements:**
- Python `lxml` library

**Parameters:**

| Parameter | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| path | yes | path | - | Path to the XML file |
| xpath | no* | str | - | XPath expression to locate element |
| value | no | str | - | Text value to set |
| attributes | no | dict | - | Dictionary of attributes to set |
| task_block | no* | list | - | List of operations to apply |
| xml_set_raw | no | str | - | Raw XML string to replace element |
| when_xpath_exist | no | str | - | Only perform if xpath exists |
| backup | no | bool | false | Create backup before modifying |

\* Either `xpath` or `task_block` must be provided

**Example:**

```yaml
- name: Set Wazuh server address
  pyurin.utils.ossconf_edit:
    path: /var/ossec/etc/ossec.conf
    xpath: /ossec_config/client/server/address
    value: "192.168.1.100"
    backup: true
```

## Testing

Test playbooks are available in the `playbooks/` directory:

```bash
# Test wazuh_dashboard_saved_search module
ansible-playbook playbooks/test_wazuh_dashboard_saved_search.yml \
  -e dashboard_host=192.168.1.100 \
  -e dashboard_username=admin \
  -e dashboard_password=SecretPassword123
```

## Development

To add a new module:

1. Create the module file in `plugins/modules/`
2. Add corresponding module_utils in `plugins/module_utils/` if needed
3. Follow Ansible module development best practices
4. Include DOCUMENTATION, EXAMPLES, and RETURN docstrings
5. Create tests in `playbooks/` or `plugins/module_utils/test/`
