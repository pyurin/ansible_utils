"""
Core OpenSearch API utility functions for Wazuh Dashboard interactions
"""
import requests, time, urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_dashboard_url(dashboard_host, port=443):
    """
    Construct the dashboard URL from host and port

    Args:
        dashboard_host: Hostname or IP of the dashboard
        port: Port number (default: 443)

    Returns:
        str: Full dashboard URL
    """
    return f"https://{dashboard_host}:{port}"


def get_opensearch_headers():
    """
    Get standard headers for OpenSearch API requests

    Returns:
        dict: Headers dictionary with required fields
    """
    return {
        "osd-xsrf": "true",
        "Content-Type": "application/json"
    }


def make_opensearch_request(method, url, username, password, **kwargs):
    """
    Make an authenticated request to OpenSearch API

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        url: Full URL for the API endpoint
        username: Dashboard username
        password: Dashboard password
        **kwargs: Additional arguments passed to requests.request()

    Returns:
        requests.Response: Response object

    Raises:
        requests.exceptions.RequestException: On connection or request errors
    """
    # Ensure headers are set
    if 'headers' not in kwargs:
        kwargs['headers'] = get_opensearch_headers()

    # Set authentication
    kwargs['auth'] = (username, password)

    # Disable SSL verification for self-signed certs
    kwargs['verify'] = False

    return requests.request(method, url, **kwargs)


def create_saved_object(dashboard_host, object_type, object_data, username, password, port=443):
    """
    Create a saved object in OpenSearch Dashboards

    Args:
        dashboard_host: Hostname or IP of the dashboard
        object_type: Type of saved object (e.g., 'search', 'visualization', 'dashboard')
        object_data: Dictionary containing the object attributes
        username: Dashboard username
        password: Dashboard password
        port: Port number (default: 443)

    Returns:
        tuple: (success: bool, response_data: dict or None, error_message: str or None)
    """
    dashboard_url = get_dashboard_url(dashboard_host, port)
    url = f"{dashboard_url}/api/saved_objects/{object_type}"

    try:
        response = make_opensearch_request(
            'POST',
            url,
            username,
            password,
            json=object_data
        )

        if response.status_code == 200:
            return True, response.json(), None
        else:
            error_msg = f"Status code: {response.status_code}, Response: {response.text}"
            return False, None, error_msg

    except requests.exceptions.ConnectionError:
        error_msg = f"Could not connect to Wazuh Dashboard at {dashboard_url}"
        return False, None, error_msg
    except Exception as e:
        return False, None, str(e)


def get_saved_object(dashboard_host, object_type, object_id, username, password, port=443):
    """
    Retrieve a saved object from OpenSearch Dashboards

    Args:
        dashboard_host: Hostname or IP of the dashboard
        object_type: Type of saved object
        object_id: ID of the object to retrieve
        username: Dashboard username
        password: Dashboard password
        port: Port number (default: 443)

    Returns:
        tuple: (success: bool, response_data: dict or None, error_message: str or None)
    """
    dashboard_url = get_dashboard_url(dashboard_host, port)
    url = f"{dashboard_url}/api/saved_objects/{object_type}/{object_id}"

    try:
        response = make_opensearch_request(
            'GET',
            url,
            username,
            password
        )

        if response.status_code == 200:
            return True, response.json(), None
        else:
            error_msg = f"Status code: {response.status_code}, Response: {response.text}"
            return False, None, error_msg

    except requests.exceptions.ConnectionError:
        error_msg = f"Could not connect to Wazuh Dashboard at {dashboard_url}"
        return False, None, error_msg
    except Exception as e:
        return False, None, str(e)


def update_saved_object(dashboard_host, object_type, object_id, object_data, username, password, port=443):
    """
    Update a saved object in OpenSearch Dashboards

    Args:
        dashboard_host: Hostname or IP of the dashboard
        object_type: Type of saved object
        object_id: ID of the object to update
        object_data: Dictionary containing the object attributes to update
        username: Dashboard username
        password: Dashboard password
        port: Port number (default: 443)

    Returns:
        tuple: (success: bool, response_data: dict or None, error_message: str or None)
    """
    dashboard_url = get_dashboard_url(dashboard_host, port)
    url = f"{dashboard_url}/api/saved_objects/{object_type}/{object_id}"

    try:
        response = make_opensearch_request(
            'PUT',
            url,
            username,
            password,
            json=object_data
        )

        if response.status_code == 200:
            return True, response.json(), None
        else:
            error_msg = f"Status code: {response.status_code}, Response: {response.text}"
            return False, None, error_msg

    except requests.exceptions.ConnectionError:
        error_msg = f"Could not connect to Wazuh Dashboard at {dashboard_url}"
        return False, None, error_msg
    except Exception as e:
        return False, None, str(e)


def delete_saved_object(dashboard_host, object_type, object_id, username, password, port=443):
    """
    Delete a saved object from OpenSearch Dashboards

    Args:
        dashboard_host: Hostname or IP of the dashboard
        object_type: Type of saved object
        object_id: ID of the object to delete
        username: Dashboard username
        password: Dashboard password
        port: Port number (default: 443)

    Returns:
        tuple: (success: bool, response_data: dict or None, error_message: str or None)
    """
    dashboard_url = get_dashboard_url(dashboard_host, port)
    url = f"{dashboard_url}/api/saved_objects/{object_type}/{object_id}"

    try:
        response = make_opensearch_request(
            'DELETE',
            url,
            username,
            password
        )

        if response.status_code == 200:
            return True, response.json(), None
        else:
            error_msg = f"Status code: {response.status_code}, Response: {response.text}"
            return False, None, error_msg

    except requests.exceptions.ConnectionError:
        error_msg = f"Could not connect to Wazuh Dashboard at {dashboard_url}"
        return False, None, error_msg
    except Exception as e:
        return False, None, str(e)

def wait_dashboard_ready(dashboard_host, port=443):
    url = get_dashboard_url(dashboard_host, port)
    for i in range(30):
        try:
            response = requests.get(url, timeout=1, verify=False)
            if 200 <= response.status_code < 400:
                break
        except:
            pass
        time.sleep(5)

def find_saved_objects(dashboard_host, object_type, search_term=None, username=None, password=None, port=443):
    """
    Find saved objects in OpenSearch Dashboards

    Args:
        dashboard_host: Hostname or IP of the dashboard
        object_type: Type of saved object (e.g., 'search', 'visualization', 'dashboard')
        search_term: Optional search term to filter by title
        username: Dashboard username
        password: Dashboard password
        port: Port number (default: 443)

    Returns:
        tuple: (success: bool, saved_objects_list: list or None, error_message: str or None)
    """
    dashboard_url = get_dashboard_url(dashboard_host, port)
    url = f"{dashboard_url}/api/saved_objects/_find"

    # Build query parameters
    params = {
        'type': object_type,
        'per_page': 10000  # Set high to get all results
    }

    if search_term:
        params['search'] = search_term
        params['search_fields'] = 'title'

    try:
        response = make_opensearch_request(
            'GET',
            url,
            username,
            password,
            params=params
        )

        if response.status_code == 200:
            data = response.json()
            return True, data.get('saved_objects', []), None
        else:
            error_msg = f"Status code: {response.status_code}, Response: {response.text}"
            return False, None, error_msg

    except requests.exceptions.ConnectionError:
        error_msg = f"Could not connect to Wazuh Dashboard at {dashboard_url}"
        return False, None, error_msg
    except Exception as e:
        return False, None, str(e)
