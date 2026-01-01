"""
Script to create a Wazuh Saved Search using OpenSearch Dashboards API
"""
import json, sys, re, os
import importlib.util
from pathlib import Path
module_path = Path(__file__).parent / "utils" / "helpers.py"

# print(__file__)  # Commented out - breaks Ansible module JSON output
from .api import create_saved_object, find_saved_objects, update_saved_object, wait_dashboard_ready

# Default configuration
INDEX_PATTERN_ID = "wazuh-alerts-*"  # Default Wazuh index pattern

def parse_filter_string(filter_string):
    """
    Parse a simple filter string into OpenSearch filter objects

    Args:
        filter_string: Simple filter string (e.g., 'agent.name:Mac-mini.local and not rule.groups:auth_failed')

    Returns:
        list: List of filter objects in OpenSearch format
    """
    if not filter_string or filter_string.strip() == "":
        return []

    filters = []

    # Split by ' and ' to get individual conditions
    conditions = re.split(r'\s+and\s+', filter_string.strip())

    for condition in conditions:
        condition = condition.strip()

        # Check if this is a negated condition
        negate = False
        if condition.startswith('not '):
            negate = True
            condition = condition[4:].strip()  # Remove 'not ' prefix

        # Parse field:value or field:"value" pattern
        # Supports both quoted and unquoted values
        match = re.match(r'([a-zA-Z0-9_.]+)\s*:\s*(?:"([^"]*)"|(\S+))', condition)
        if match:
            field_name = match.group(1)
            # Use quoted value (group 2) if present, otherwise unquoted value (group 3)
            field_value = match.group(2) if match.group(2) is not None else match.group(3)

            # Create filter object
            filter_obj = {
                "meta": {
                    "alias": None,
                    "disabled": False,
                    "negate": negate,
                    "key": field_name,
                    "type": "phrase",
                    "params": {
                        "query": field_value
                    },
                    "index": INDEX_PATTERN_ID
                },
                "query": {
                    "match_phrase": {
                        field_name: field_value
                    }
                },
                "$state": {
                    "store": "appState"
                }
            }
            filters.append(filter_obj)

    return filters

def create_saved_search(dashboard_host, username, password, saved_search_title, filter=None, columns=None, description=None, port=443):
    """
    Create or update a saved search in OpenSearch Dashboards

    Args:
        dashboard_host: Hostname or IP of the dashboard
        username: Dashboard username
        password: Dashboard password
        saved_search_title: Title for the saved search
        filter: Simple filter string (e.g., 'agent.name:Mac-mini.local and not rule.groups:authentication_failed')
                If None, no filters are applied (default: None)
        columns: List of columns to display (default: ["timestamp", "agent.name", "rule.description", "rule.level", "rule.id"])
        description: Description for the saved search (default: uses saved_search_title)
        port: Port number (default: 443)
    """
    # print(f"dashboard_host = {dashboard_host}, username = {username}, password = {password}")
    # Set default columns if not provided
    if columns is None:
        columns = ["timestamp", "agent.name", "rule.description", "rule.level", "rule.id"]

    # Set default description if not provided
    if description is None:
        description = saved_search_title

    # print(f"Creating saved search on Wazuh Dashboard. Title: {saved_search_title}")
    # if filter:
    #     print(f"Filter: {filter}")

    # Parse filter string into filter objects
    filter_objects = parse_filter_string(filter) if filter else []

    # Saved search object
    saved_search_object = {
        "attributes": {
            "title": saved_search_title,
            "description": description,
            "hits": 0,
            "columns": columns,
            "sort": [["timestamp", "desc"]],
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "index": INDEX_PATTERN_ID,
                    "query": {
                        "query": "",
                        "language": "kuery"
                    },
                    "filter": filter_objects,
                    "highlightAll": True,
                    "version": True
                })
            }
        }
    }

    wait_dashboard_ready(
        dashboard_host=dashboard_host,
        port=port
    )

    # Check if a saved search with this title already exists
    # print(f"Checking for existing saved searches with title: {saved_search_title}")
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
        # Filter to exact title match (search might return partial matches)
        exact_matches = [obj for obj in existing_objects
                        if obj.get('attributes', {}).get('title') == saved_search_title]

        if exact_matches:
            # Use the first exact match
            existing_object_id = exact_matches[0].get('id')
            # print(f"Found existing saved search with ID: {existing_object_id}. Updating...")

    # Update existing saved search or create a new one
    if existing_object_id:
        success, result, error = update_saved_object(
            dashboard_host=dashboard_host,
            object_type='search',
            object_id=existing_object_id,
            object_data=saved_search_object,
            username=username,
            password=password,
            port=port
        )

        if success:
            # print(f"✓ Saved search updated successfully!")
            # print(f"  ID: {result.get('id')}, title: {saved_search_title}")
            pass
        else:
            raise Exception(f"Failed to update saved search: {error}")
    else:
        success, result, error = create_saved_object(
            dashboard_host=dashboard_host,
            object_type='search',
            object_data=saved_search_object,
            username=username,
            password=password,
            port=port
        )

        if success:
            # print(f"✓ Saved search created successfully!")
            # print(f"  ID: {result.get('id')}, title: {saved_search_title}")
            pass
        else:
            raise Exception(f"Failed to create saved search: {error}")

if __name__ == "__main__":
    # Configuration
    args = sys.argv[1:]
    if args[5] != '':
        args[5] = json.loads(args[5])
    create_saved_search(*args)
