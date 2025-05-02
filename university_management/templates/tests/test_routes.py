import pytest
import json
from {service_name}.models import *

def test_get_resource(client, auth_headers, test_token):
    """Test GET resource endpoint."""
    headers = auth_headers(test_token)
    response = client.get('/api/v1/{service_name}/resource/1', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'data' in data
    assert isinstance(data['data'], dict)

def test_create_resource(client, auth_headers, test_token):
    """Test POST resource endpoint."""
    headers = auth_headers(test_token)
    data = {
        'field1': 'value1',
        'field2': 123
    }
    response = client.post(
        '/api/v1/{service_name}/resource',
        headers=headers,
        json=data
    )
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'data' in response_data
    assert response_data['data']['field1'] == 'value1'

def test_update_resource(client, auth_headers, test_token):
    """Test PUT resource endpoint."""
    headers = auth_headers(test_token)
    data = {
        'field1': 'updated_value',
        'field2': 456
    }
    response = client.put(
        '/api/v1/{service_name}/resource/1',
        headers=headers,
        json=data
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['data']['field1'] == 'updated_value'

def test_delete_resource(client, auth_headers, test_token):
    """Test DELETE resource endpoint."""
    headers = auth_headers(test_token)
    response = client.delete(
        '/api/v1/{service_name}/resource/1',
        headers=headers
    )
    assert response.status_code == 204

def test_list_resources(client, auth_headers, test_token):
    """Test GET list resources endpoint."""
    headers = auth_headers(test_token)
    response = client.get(
        '/api/v1/{service_name}/resource',
        headers=headers,
        query_string={'page': 1, 'per_page': 10}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'data' in data
    assert isinstance(data['data'], list)

def test_unauthorized_access(client):
    """Test unauthorized access to protected endpoints."""
    response = client.get('/api/v1/{service_name}/resource/1')
    assert response.status_code == 401

def test_invalid_data(client, auth_headers, test_token):
    """Test handling of invalid data."""
    headers = auth_headers(test_token)
    data = {
        'field1': '',  # Invalid empty value
        'field2': -1   # Invalid negative value
    }
    response = client.post(
        '/api/v1/{service_name}/resource',
        headers=headers,
        json=data
    )
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert 'errors' in response_data

def test_not_found(client, auth_headers, test_token):
    """Test handling of non-existent resources."""
    headers = auth_headers(test_token)
    response = client.get(
        '/api/v1/{service_name}/resource/999',
        headers=headers
    )
    assert response.status_code == 404

def test_search_resources(client, auth_headers, test_token):
    """Test search functionality."""
    headers = auth_headers(test_token)
    response = client.get(
        '/api/v1/{service_name}/resource/search',
        headers=headers,
        query_string={'q': 'search_term', 'page': 1}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'data' in data
    assert isinstance(data['data'], list)

def test_filter_resources(client, auth_headers, test_token):
    """Test filtering functionality."""
    headers = auth_headers(test_token)
    response = client.get(
        '/api/v1/{service_name}/resource',
        headers=headers,
        query_string={'field1': 'value1', 'field2': 123}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'data' in data
    assert isinstance(data['data'], list)

def test_sort_resources(client, auth_headers, test_token):
    """Test sorting functionality."""
    headers = auth_headers(test_token)
    response = client.get(
        '/api/v1/{service_name}/resource',
        headers=headers,
        query_string={'sort_by': 'field1', 'sort_order': 'asc'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'data' in data
    assert isinstance(data['data'], list)

def test_bulk_operations(client, auth_headers, test_token):
    """Test bulk operations."""
    headers = auth_headers(test_token)
    data = [
        {'field1': 'value1', 'field2': 123},
        {'field1': 'value2', 'field2': 456}
    ]
    response = client.post(
        '/api/v1/{service_name}/resource/bulk',
        headers=headers,
        json=data
    )
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'data' in response_data
    assert len(response_data['data']) == 2 