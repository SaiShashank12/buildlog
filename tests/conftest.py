"""
Shared test fixtures and configuration
"""
import os

# Set test environment variables BEFORE any imports
os.environ['APPWRITE_ENDPOINT'] = 'https://test.appwrite.io/v1'
os.environ['APPWRITE_PROJECT_ID'] = 'test_project_id'
os.environ['APPWRITE_API_KEY'] = 'test_api_key'
os.environ['APPWRITE_DATABASE_ID'] = 'test_database'
os.environ['APPWRITE_PROJECTS_COLLECTION_ID'] = 'test_projects'
os.environ['APPWRITE_BUILD_LOGS_COLLECTION_ID'] = 'test_logs'
os.environ['APPWRITE_STORAGE_BUCKET_ID'] = 'test_storage'
os.environ['SECRET_KEY'] = 'test_secret_key_for_testing'
os.environ['DEBUG'] = 'True'

import pytest
from unittest.mock import patch


@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        'name': 'Test Project',
        'description': 'A test project for unit testing',
        'tech_stack': ['Python', 'FastAPI', 'Appwrite'],
        'repository_url': 'https://github.com/test/repo',
        'demo_url': 'https://demo.test.com',
        'tags': ['test', 'demo', 'hackathon'],
        'status': 'in_progress',
        'user_id': 'test_user_123',
        'created_at': '2025-10-13T12:00:00',
        'updated_at': '2025-10-13T12:00:00'
    }


@pytest.fixture
def sample_build_log_data():
    """Sample build log data for testing"""
    return {
        'project_id': 'test_project_123',
        'title': 'Test Build Log',
        'content': 'This is a test build log entry with some content.',
        'log_type': 'update',
        'code_snippets': [
            {'language': 'python', 'code': 'print("Hello, World!")'}
        ],
        'images': ['image1.jpg', 'image2.png'],
        'links': [
            {'title': 'GitHub', 'url': 'https://github.com'}
        ],
        'tags': ['test', 'progress'],
        'created_at': '2025-10-13T14:30:00'
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        '$id': 'test_user_123',
        'email': 'test@example.com',
        'name': 'Test User'
    }


@pytest.fixture
def mock_current_user(sample_user_data):
    """Mock the current user"""
    with patch('main.get_current_user') as mock:
        mock.return_value = sample_user_data
        yield mock
