#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Petr Iurin <p.yurin@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import yaml

def yamledit(yaml_content, key, separator='.', value=None, state='present', append_unique=False):
    """
    Edit YAML content by setting or removing values at a specific key path.

    Args:
        yaml_content (str): YAML content as a string
        key (str): Path to the element in YAML, separated by separator
        separator (str): Separator for the key path (default: '.')
        value: Value to set (can be scalar, list, or dict). Ignored if state='absent'
        state (str): 'present' to set value, 'absent' to remove element
        append_unique (bool): If True, append value to list only if it doesn't exist

    Returns:
        str: Modified YAML content

    Raises:
        ValueError: If key is invalid or empty, or if append_unique is used with non-list
    """

    if not key:
        raise ValueError("key parameter cannot be empty")

    # Parse YAML content
    try:
        data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML content: {str(e)}")

    # If data is None (empty file), initialize as empty dict
    if data is None:
        data = {}

    # Split key by separator
    key_parts = key.split(separator)

    # Navigate to the target location
    if state == 'absent':
        # For absent state, we need to remove the key
        _remove_value(data, key_parts)
    elif append_unique:
        # For append_unique mode, append value to list if unique
        _append_unique_value(data, key_parts, value)
    else:
        # For present state, set the value
        _set_value(data, key_parts, value)

    # Convert back to YAML
    return yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)


def _set_value(data, key_parts, value):
    """
    Set a value in nested dict/list structure.

    Args:
        data: The root data structure (dict or list)
        key_parts: List of key parts representing the path
        value: Value to set
    """
    current = data

    # Navigate to the parent of the target
    for i, part in enumerate(key_parts[:-1]):
        # Check if part is a list index
        if _is_list_index(part):
            index = int(part)
            # Ensure current is a list
            if not isinstance(current, list):
                raise ValueError(f"Expected list at '{'.'.join(key_parts[:i])}', but found {type(current).__name__}")

            # Extend list if needed
            while len(current) <= index:
                current.append(None)

            # Get or create the next level
            if current[index] is None:
                # Determine what to create based on next part
                next_part = key_parts[i + 1]
                if _is_list_index(next_part):
                    current[index] = []
                else:
                    current[index] = {}

            current = current[index]
        else:
            # Dictionary key
            if not isinstance(current, dict):
                raise ValueError(f"Expected dict at '{'.'.join(key_parts[:i])}', but found {type(current).__name__}")

            # Create next level if it doesn't exist
            if part not in current:
                # Determine what to create based on next part
                next_part = key_parts[i + 1]
                if _is_list_index(next_part):
                    current[part] = []
                else:
                    current[part] = {}

            current = current[part]

    # Set the final value
    final_key = key_parts[-1]

    if _is_list_index(final_key):
        index = int(final_key)
        if not isinstance(current, list):
            raise ValueError(f"Expected list at '{'.'.join(key_parts[:-1])}', but found {type(current).__name__}")

        # Extend list if needed
        while len(current) <= index:
            current.append(None)

        current[index] = value
    else:
        if not isinstance(current, dict):
            raise ValueError(f"Expected dict at '{'.'.join(key_parts[:-1])}', but found {type(current).__name__}")

        current[final_key] = value


def _remove_value(data, key_parts):
    """
    Remove a value from nested dict/list structure.

    Args:
        data: The root data structure (dict or list)
        key_parts: List of key parts representing the path
    """
    if not key_parts:
        return

    current = data
    path = []

    # Navigate to the parent of the target
    for i, part in enumerate(key_parts[:-1]):
        path.append((current, part))

        if _is_list_index(part):
            index = int(part)
            if not isinstance(current, list) or len(current) <= index:
                # Path doesn't exist, nothing to remove
                return
            current = current[index]
        else:
            if not isinstance(current, dict) or part not in current:
                # Path doesn't exist, nothing to remove
                return
            current = current[part]

    # Remove the final key
    final_key = key_parts[-1]

    if _is_list_index(final_key):
        index = int(final_key)
        if isinstance(current, list) and len(current) > index:
            current.pop(index)
    else:
        if isinstance(current, dict) and final_key in current:
            del current[final_key]


def _append_unique_value(data, key_parts, value):
    """
    Append a value to a list only if it doesn't already exist.
    Creates an empty list if the key doesn't exist.

    Args:
        data: The root data structure (dict or list)
        key_parts: List of key parts representing the path
        value: Value to append to the list

    Raises:
        ValueError: If the key exists but is not a list
    """
    current = data

    # Navigate to the parent of the target
    for i, part in enumerate(key_parts[:-1]):
        # Check if part is a list index
        if _is_list_index(part):
            index = int(part)
            # Ensure current is a list
            if not isinstance(current, list):
                raise ValueError(f"Expected list at '{'.'.join(key_parts[:i])}', but found {type(current).__name__}")

            # Extend list if needed
            while len(current) <= index:
                current.append(None)

            # Get or create the next level
            if current[index] is None:
                # Determine what to create based on next part
                next_part = key_parts[i + 1]
                if _is_list_index(next_part):
                    current[index] = []
                else:
                    current[index] = {}

            current = current[index]
        else:
            # Dictionary key
            if not isinstance(current, dict):
                raise ValueError(f"Expected dict at '{'.'.join(key_parts[:i])}', but found {type(current).__name__}")

            # Create next level if it doesn't exist
            if part not in current:
                # Determine what to create based on next part
                next_part = key_parts[i + 1]
                if _is_list_index(next_part):
                    current[part] = []
                else:
                    current[part] = {}

            current = current[part]

    # Handle the final key
    final_key = key_parts[-1]

    if _is_list_index(final_key):
        # Can't use append_unique with list index
        raise ValueError(f"append_unique cannot be used with list index '{final_key}'")
    else:
        if not isinstance(current, dict):
            raise ValueError(f"Expected dict at '{'.'.join(key_parts[:-1])}', but found {type(current).__name__}")

        # Check if key exists
        if final_key not in current:
            # Key doesn't exist, create empty list
            current[final_key] = []

        # Ensure the value is a list
        if not isinstance(current[final_key], list):
            raise ValueError(f"Key '{'.'.join(key_parts)}' exists but is not a list (found {type(current[final_key]).__name__})")

        # Append value if it's not already in the list
        if value not in current[final_key]:
            current[final_key].append(value)


def _is_list_index(key_part):
    """
    Check if a key part represents a list index (is a number).

    Args:
        key_part (str): Key part to check

    Returns:
        bool: True if key_part is a valid list index
    """
    try:
        int(key_part)
        return True
    except ValueError:
        return False
