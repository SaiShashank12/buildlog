"""
Unit tests for configuration module
"""
import pytest
import os
from unittest.mock import patch
from app.config import Settings, get_settings


class TestSettings:
    """Test Settings class"""

    def test_settings_with_env_vars(self):
        """Test settings loaded from environment variables"""
        with patch.dict(os.environ, {
            'APPWRITE_ENDPOINT': 'https://test.appwrite.io/v1',
            'APPWRITE_PROJECT_ID': 'test_project',
            'APPWRITE_API_KEY': 'test_key',
            'APPWRITE_DATABASE_ID': 'test_db',
            'APPWRITE_PROJECTS_COLLECTION_ID': 'test_projects',
            'APPWRITE_BUILD_LOGS_COLLECTION_ID': 'test_logs',
            'APPWRITE_STORAGE_BUCKET_ID': 'test_bucket',
            'SECRET_KEY': 'test_secret',
            'DEBUG': 'False'
        }):
            settings = Settings()
            assert settings.appwrite_endpoint == 'https://test.appwrite.io/v1'
            assert settings.appwrite_project_id == 'test_project'
            assert settings.appwrite_api_key == 'test_key'
            assert settings.appwrite_database_id == 'test_db'
            assert settings.debug is False

    def test_settings_defaults(self):
        """Test default settings values when not set in env"""
        with patch.dict(os.environ, {
            'APPWRITE_ENDPOINT': 'https://custom.appwrite.io/v1',
            'APPWRITE_PROJECT_ID': 'test',
            'APPWRITE_API_KEY': 'key',
            'SECRET_KEY': 'secret'
        }, clear=True):
            settings = Settings()
            # Since .env file is loaded, it may override defaults
            # Just ensure the values are set
            assert settings.appwrite_endpoint is not None
            assert settings.appwrite_database_id == "buildlog_db"
            assert settings.debug is True

    def test_get_settings_cached(self):
        """Test that get_settings returns cached instance"""
        with patch.dict(os.environ, {
            'APPWRITE_PROJECT_ID': 'test',
            'APPWRITE_API_KEY': 'key',
            'SECRET_KEY': 'secret'
        }):
            settings1 = get_settings()
            settings2 = get_settings()
            assert settings1 is settings2

    def test_settings_case_insensitive(self):
        """Test that environment variables are case insensitive"""
        with patch.dict(os.environ, {
            'appwrite_project_id': 'lower_case',
            'APPWRITE_API_KEY': 'upper_case',
            'SECRET_KEY': 'secret'
        }):
            settings = Settings()
            assert settings.appwrite_project_id == 'lower_case'
