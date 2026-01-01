#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Petr Iurin <p.yurin@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys, re, json
from lxml import etree


def split_xpath(xpath):
    """Split xpath by '/' but not when inside predicates (square brackets)."""
    parts = []
    current_part = ""
    bracket_depth = 0

    for char in xpath:
        if char == '[':
            bracket_depth += 1
            current_part += char
        elif char == ']':
            bracket_depth -= 1
            current_part += char
        elif char == '/' and bracket_depth == 0:
            if current_part:
                parts.append(current_part)
            current_part = ""
        else:
            current_part += char

    if current_part:
        parts.append(current_part)

    return parts

def convert_xml_content(buf):
    return re.sub('&', '--AMP-SYMBOL-SUBST--', buf)

def convert_xml_content_back(buf):
    return re.sub('--AMP-SYMBOL-SUBST--', '&', buf)



def extract_tag_name(xpath_part):
    """Extract tag name from xpath part, removing predicates."""
    # Remove predicates like [location=journald]
    match = re.match(r'^([^\[]+)', xpath_part)
    if match:
        return match.group(1)
    return xpath_part


def parse_predicate(xpath_part):
    """Parse predicate from xpath part like 'localfile[@location='journald']' or 'integration[name='test']'
    Returns (tag_name, predicate_type, predicate_dict) where predicate_type is 'attr' or 'child' or None"""
    # Match predicates with @ (attribute) or without (child element)
    match = re.match(r'^([^\[]+)(?:\[(@?)([^=]+)=\'([^\']+)\'\])?', xpath_part)
    if match:
        tag_name = match.group(1)
        if match.group(2) is not None and match.group(3) and match.group(4):
            # Has predicate
            has_at_sign = match.group(2) == '@'
            pred_name = match.group(3)
            pred_value = match.group(4)
            predicate_type = 'attr' if has_at_sign else 'child'
            return tag_name, predicate_type, {pred_name: pred_value}
        return tag_name, None, None
    return xpath_part, None, None


def ossconf_edit(xml_content, xpath=None, value=None, attributes=None, task_block=None, xml_set_raw=None, when_xpath_exist=None):

    # in ansible we pass empty string instead of None
    if xpath == '':
        xpath = None
    if value == '':
        value = None
    if attributes == '':
        attributes = None
    if task_block == '':
        task_block = None
    if xml_set_raw == '':
        xml_set_raw = None
    if when_xpath_exist == '':
        when_xpath_exist = None
    if attributes is not None and isinstance(attributes, str):
        attributes = json.loads(attributes)
    # If task_block is provided, apply each operation in sequence
    if task_block is not None:
        result = xml_content
        for operation in task_block:
            op_xpath = operation.get('xpath')
            op_value = operation.get('value', None)
            op_attributes = operation.get('attributes', None)
            op_set_raw = operation.get('xml_set_raw', None)
            op_when_xpath_exist = operation.get('when_xpath_exist', None)
            result = ossconf_edit(result, op_xpath, op_value, op_attributes, xml_set_raw=op_set_raw, when_xpath_exist=op_when_xpath_exist)
        return result

    # Single operation mode
    if xpath is None:
        raise ValueError("xpath is required when task_block is not provided")

    # Wrap provided XML in 'root' node
    wrapped_xml = convert_xml_content('<root>' + xml_content + '</root>')

    # Parse XML with lxml
    root = etree.fromstring(wrapped_xml.encode('utf-8'))

    # Check if when_xpath_exist is provided and if the xpath exists
    if when_xpath_exist is not None:
        # Adjust when_xpath_exist to account for root wrapper
        if when_xpath_exist.startswith('/'):
            check_xpath = '/root' + when_xpath_exist
        else:
            check_xpath = when_xpath_exist

        # Check if the xpath exists
        matching_nodes = root.xpath(check_xpath)

        # If the xpath doesn't exist, return the original XML unchanged
        if not matching_nodes:
            return xml_content

    # Handle xml_set_raw - completely replace the targeted node(s) with raw XML
    if xml_set_raw is not None:
        # Extract XML string from set if needed
        if isinstance(xml_set_raw, set):
            xml_set_raw = list(xml_set_raw)[0]

        # Parse the raw XML string
        raw_xml_str = xml_set_raw.strip()
        raw_element = etree.fromstring(convert_xml_content(raw_xml_str).encode('utf-8'))

        # Adjust xpath to account for root wrapper
        if xpath.startswith('/'):
            full_xpath = '/root' + xpath
        else:
            full_xpath = xpath

        # Find existing nodes matching the xpath
        matching_nodes = root.xpath(full_xpath)

        if matching_nodes:
            # Replace the first matching node
            parent = matching_nodes[0].getparent()
            index = list(parent).index(matching_nodes[0])
            parent.remove(matching_nodes[0])
            parent.insert(index, raw_element)
        else:
            # Node doesn't exist, need to create it
            # Split xpath to find where to insert
            parts = split_xpath(full_xpath)

            # Find the deepest existing parent
            parent_nodes = []
            parent_index = 0

            for i in range(len(parts), 0, -1):
                test_xpath = '/' + '/'.join(parts[:i])
                test_nodes = root.xpath(test_xpath)

                if test_nodes:
                    parent_nodes = test_nodes
                    parent_index = i
                    break

            # If no parent found, use root
            if not parent_nodes:
                parent_nodes = [root]
                parent_index = 1  # Skip /root

            # We only insert at the first matching parent
            parent = parent_nodes[0]
            parent.append(raw_element)

        # Return XML as UTF-8 string (without root node and xml declaration)
        result_parts = [etree.tostring(child, encoding='utf-8', pretty_print=True).decode('utf-8').rstrip() for child in root]
        return convert_xml_content_back('\n'.join(result_parts))

    # Open node with xpath and set value to value
    # Adjust xpath to account for root wrapper
    if xpath.startswith('/'):
        full_xpath = '/root' + xpath
    else:
        full_xpath = xpath

    # Split xpath into parts to understand what we're trying to set
    parts = split_xpath(full_xpath)

    # Find the parent path (all but the last element)
    if len(parts) > 1:
        parent_xpath = '/' + '/'.join(parts[:-1])
        target_part = parts[-1]
    else:
        parent_xpath = None
        target_part = parts[0] if parts else None

    # Find all parent nodes where we should set/update the target
    if parent_xpath:
        parent_nodes = root.xpath(parent_xpath)
    else:
        parent_nodes = [root]

    if not parent_nodes:
        # No parent nodes exist, need to create the full path
        # Find the deepest existing parent
        parent_nodes = []
        parent_index = 0

        # Start from less specific (beginning) and go to more specific (end)
        for i in range(1, len(parts)):
            test_xpath = '/' + '/'.join(parts[:i])
            test_nodes = root.xpath(test_xpath)

            if test_nodes:
                # Nodes found at this level
                parent_nodes = test_nodes
                parent_index = i
            else:
                # No nodes found, stop here
                break

        # If no parent found, start from root
        if not parent_nodes:
            parent_nodes = [root]
            parent_index = 0

        # For each parent node, create the remaining path
        for parent in parent_nodes:
            current = parent
            # Create all remaining levels
            for i in range(parent_index, len(parts)):
                tag_name, predicate_type, predicate = parse_predicate(parts[i])

                # Check if child already exists (for both intermediate and final nodes)
                existing_child = None
                if predicate:
                    # Has predicate, need to find matching child
                    if predicate_type == 'attr':
                        # Attribute predicate
                        matching_children = [
                            child for child in current.findall(tag_name)
                            if all(child.get(k) == v for k, v in predicate.items())
                        ]
                        if matching_children:
                            existing_child = matching_children[0]
                    else:
                        # Child element predicate
                        matching_children = [
                            child for child in current.findall(tag_name)
                            if all(
                                child.find(k) is not None and child.find(k).text == v
                                for k, v in predicate.items()
                            )
                        ]
                        if matching_children:
                            existing_child = matching_children[0]
                else:
                    # No predicate, just find by tag
                    existing_child = current.find(tag_name)

                if existing_child is not None:
                    # Child exists, use it
                    current = existing_child
                    # If this is the final element and we're setting a value, update it
                    if i == len(parts) - 1:
                        if attributes:
                            for attr_name, attr_value in attributes.items():
                                existing_child.set(attr_name, attr_value)
                        if value is not None:
                            existing_child.text = value
                    continue

                # Create new element
                new_element = etree.SubElement(current, tag_name)

                # Set predicate attributes/children if this is an intermediate node with predicates
                if predicate:
                    if predicate_type == 'attr':
                        # Set attributes
                        for attr_name, attr_value in predicate.items():
                            new_element.set(attr_name, attr_value)
                    elif predicate_type == 'child' and i < len(parts) - 1:
                        # Create child elements only for intermediate nodes
                        # Not for the final target node (that gets handled separately)
                        for child_name, child_value in predicate.items():
                            child_elem = etree.SubElement(new_element, child_name)
                            child_elem.text = child_value

                # If this is the last element, set value or attributes
                if i == len(parts) - 1:
                    if attributes:
                        for attr_name, attr_value in attributes.items():
                            new_element.set(attr_name, attr_value)
                    if value is not None:
                        new_element.text = value

                current = new_element
    else:
        # Parent nodes exist, set/update the target element in each
        for parent in parent_nodes:
            tag_name, predicate_type, predicate = parse_predicate(target_part)

            # Check if target already exists in this parent
            if predicate:
                if predicate_type == 'attr':
                    # Attribute predicate - find matching child
                    matching_children = [
                        child for child in parent.findall(tag_name)
                        if all(child.get(k) == v for k, v in predicate.items())
                    ]
                    if matching_children:
                        target_node = matching_children[0]
                    else:
                        # Create new element with predicate
                        target_node = etree.SubElement(parent, tag_name)
                        for attr_name, attr_value in predicate.items():
                            target_node.set(attr_name, attr_value)
                else:
                    # Child element predicate - find or create
                    matching_children = [
                        child for child in parent.findall(tag_name)
                        if all(
                            child.find(k) is not None and child.find(k).text == v
                            for k, v in predicate.items()
                        )
                    ]
                    if matching_children:
                        target_node = matching_children[0]
                    else:
                        # Create new element - but don't add predicate children yet
                        # because the predicate IS the target we're trying to set
                        target_node = etree.SubElement(parent, tag_name)
            else:
                # No predicate, find or create simple element
                target_node = parent.find(tag_name)
                if target_node is None:
                    target_node = etree.SubElement(parent, tag_name)

            # Set the value or attributes on the target node
            if attributes:
                for attr_name, attr_value in attributes.items():
                    target_node.set(attr_name, attr_value)
            if value is not None:
                target_node.text = value

    # Return XML as UTF-8 string (without root node and xml declaration)
    result_parts = [etree.tostring(child, encoding='utf-8', pretty_print=True).decode('utf-8').rstrip() for child in root]

    # subst. & symbol
    return convert_xml_content_back('\n'.join(result_parts))
