import unittest
import re
import sys
from pathlib import Path

# Add wazuh directory to path to import ossconf_edit module
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'wazuh'))
# Add current directory to import test_cases
sys.path.insert(0, str(Path(__file__).parent))

from lxml import etree
from ossconf_edit import ossconf_edit, convert_xml_content
from . import test_cases as test_cases_module

test_cases = test_cases_module.test_cases


def normalize_whitespace(text):
    """Normalize whitespace by collapsing multiple newlines into max 2."""
    # Replace multiple newlines with double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip leading/trailing whitespace
    return text.strip()


def strip_whitespace_text(element):
    """Recursively strip whitespace-only text from elements."""
    # If element has only whitespace text and no children, set text to None
    if element.text and element.text.strip() == '' and len(element) == 0:
        element.text = None
    # Strip whitespace-only text between elements (tail)
    if element.tail and element.tail.strip() == '':
        element.tail = None
    # Recursively process children
    for child in element:
        strip_whitespace_text(child)


def xml_elements_equal(xml1, xml2):
    """Compare two XML strings structurally."""
    wrapped1 = convert_xml_content('<root>' + xml1.strip() + '</root>')
    wrapped2 = convert_xml_content('<root>' + xml2.strip() + '</root>')

    parser = etree.XMLParser(remove_blank_text=True)
    root1 = etree.fromstring(wrapped1.encode('utf-8'), parser)
    root2 = etree.fromstring(wrapped2.encode('utf-8'), parser)

    # Strip whitespace-only text nodes
    strip_whitespace_text(root1)
    strip_whitespace_text(root2)

    # Convert to canonical form for comparison
    c14n1 = etree.tostring(root1, method='c14n').decode('utf-8')
    c14n2 = etree.tostring(root2, method='c14n').decode('utf-8')

    return c14n1 == c14n2


class TestAssconfEdit(unittest.TestCase):

    def test_all_cases(self):
        """Test all cases from test_cases.py"""
        for i, test_case in enumerate(test_cases):
            with self.subTest(test_case_index=i):
                xml_from = test_case['xml_from']
                expected = test_case['xml_to']
                should_match = test_case.get('should_match', True)

                # Check if this is a task_block operation or single operation
                if 'task_block' in test_case:
                    # Block operation - multiple edits
                    result = ossconf_edit(xml_from, task_block=test_case['task_block'])
                else:
                    # Single operation
                    xpath = test_case['xpath']
                    value = test_case.get('value', None)
                    attributes = test_case.get('attributes', None)
                    xml_set_raw = test_case.get('xml_set_raw', None)
                    when_xpath_exist = test_case.get('when_xpath_exist', None)
                    result = ossconf_edit(xml_from, xpath, value, attributes, xml_set_raw=xml_set_raw, when_xpath_exist=when_xpath_exist)

                # Compare XML structurally
                are_equal = xml_elements_equal(result, expected)

                if should_match:
                    # Positive test: result should match expected
                    self.assertTrue(
                        are_equal,
                        f"Test case {i} failed (expected match):\n"
                        f"XPath: {test_case.get('xpath', 'N/A')}\n"
                        f"Value: {test_case.get('value', 'N/A')}\n"
                        f"Expected:\n{expected}\n\n"
                        f"Got:\n{result}"
                    )
                else:
                    # Negative test: result should NOT match expected
                    self.assertFalse(
                        are_equal,
                        f"Test case {i} failed (expected NO match):\n"
                        f"XPath: {test_case.get('xpath', 'N/A')}\n"
                        f"Value: {test_case.get('value', 'N/A')}\n"
                        f"Expected NOT to match:\n{expected}\n\n"
                        f"But got:\n{result}"
                    )


if __name__ == '__main__':
    unittest.main(verbosity=2)
