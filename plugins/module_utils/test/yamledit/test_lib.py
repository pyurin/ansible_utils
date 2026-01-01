#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Tests for yamledit module"""

import unittest
import sys
from pathlib import Path

# Add module_utils directory to path to import yamledit module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
# Add current directory to import test_cases
sys.path.insert(0, str(Path(__file__).parent))

import yaml
from yamledit import yamledit
from . import test_cases as test_cases_module

test_cases = test_cases_module.test_cases


def normalize_yaml(yaml_str):
    """
    Normalize YAML string by parsing and re-dumping it.
    This ensures consistent formatting for comparison.
    """
    if not yaml_str or yaml_str.strip() == '':
        return ''

    data = yaml.safe_load(yaml_str)
    if data is None:
        return ''

    return yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)


class TestYamlEdit(unittest.TestCase):

    def test_all_cases(self):
        """Test all cases from test_cases.py"""
        for i, test_case in enumerate(test_cases):
            with self.subTest(test_case_index=i, description=test_case.get('description', 'N/A')):
                yaml_from = test_case['yaml_from']
                expected = test_case['yaml_to']
                key = test_case['key']
                separator = test_case.get('separator', '.')
                value = test_case.get('value')
                state = test_case.get('state', 'present')
                append_unique = test_case.get('append_unique', False)

                # Execute the yamledit function
                result = yamledit(
                    yaml_content=yaml_from,
                    key=key,
                    separator=separator,
                    value=value,
                    state=state,
                    append_unique=append_unique
                )

                # Normalize both result and expected for comparison
                normalized_result = normalize_yaml(result)
                normalized_expected = normalize_yaml(expected)

                self.assertEqual(
                    normalized_result,
                    normalized_expected,
                    f"Test case {i} failed - {test_case.get('description', 'N/A')}:\n"
                    f"Key: {key}\n"
                    f"Separator: {separator}\n"
                    f"Value: {value}\n"
                    f"State: {state}\n"
                    f"Append unique: {append_unique}\n"
                    f"Expected:\n{normalized_expected}\n\n"
                    f"Got:\n{normalized_result}"
                )

    def test_empty_key_raises_error(self):
        """Test that empty key raises ValueError"""
        yaml_content = "name: test"
        with self.assertRaises(ValueError) as context:
            yamledit(yaml_content, key='', separator='.', value='value', state='present')
        self.assertIn('key parameter cannot be empty', str(context.exception))

    def test_invalid_yaml_raises_error(self):
        """Test that invalid YAML raises ValueError"""
        invalid_yaml = "name: [invalid"  # Unclosed bracket
        with self.assertRaises(ValueError) as context:
            yamledit(invalid_yaml, key='name', separator='.', value='value', state='present')
        self.assertIn('Invalid YAML content', str(context.exception))

    def test_list_index_on_dict_raises_error(self):
        """Test that using list index on dict raises ValueError"""
        yaml_content = "server:\n  host: localhost"
        with self.assertRaises(ValueError) as context:
            yamledit(yaml_content, key='server.0', separator='.', value='value', state='present')
        self.assertIn('Expected list', str(context.exception))

    def test_dict_key_on_list_raises_error(self):
        """Test that using dict key on list raises ValueError"""
        yaml_content = "items:\n  - apple\n  - banana"
        with self.assertRaises(ValueError) as context:
            yamledit(yaml_content, key='items.name', separator='.', value='value', state='present')
        self.assertIn('Expected dict', str(context.exception))

    def test_append_unique_on_non_list_raises_error(self):
        """Test that append_unique on non-list value raises ValueError"""
        yaml_content = "name: test"
        with self.assertRaises(ValueError) as context:
            yamledit(yaml_content, key='name', separator='.', value='value', state='present', append_unique=True)
        self.assertIn('not a list', str(context.exception))

    def test_append_unique_with_list_index_raises_error(self):
        """Test that append_unique with list index raises ValueError"""
        yaml_content = "items:\n  - apple\n  - banana"
        with self.assertRaises(ValueError) as context:
            yamledit(yaml_content, key='items.0', separator='.', value='value', state='present', append_unique=True)
        self.assertIn('append_unique cannot be used with list index', str(context.exception))


if __name__ == '__main__':
    unittest.main(verbosity=2)
