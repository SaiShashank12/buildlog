"""Tests for Appwrite Service"""
import pytest
from unittest.mock import Mock, patch
from app.services.appwrite_service import AppwriteService, appwrite_service


class TestAppwriteService:
    """Test Appwrite Service class"""

    def test_service_initialization(self):
        """Test service initializes correctly"""
        service = AppwriteService()
        assert service.endpoint == "https://test.appwrite.io/v1"
        assert service.project_id == "test_project_id"
        assert service.database_id == "test_database"

    def test_get_headers(self):
        """Test headers generation"""
        service = AppwriteService()
        headers = service._get_headers()
        assert "X-Appwrite-Project" in headers
        assert "X-Appwrite-Key" in headers
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"

    @patch('app.services.appwrite_service.requests.post')
    @patch('app.services.appwrite_service.ID.unique')
    def test_create_project_success(self, mock_id, mock_post):
        """Test creating a project successfully"""
        mock_id.return_value = "test_id_123"
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "$id": "test_id_123",
            "name": "Test Project",
            "user_id": "user123"
        }
        mock_post.return_value = mock_response

        service = AppwriteService()
        result = service.create_project("user123", {
            "name": "Test Project",
            "description": "Test Description",
            "created_at": "2025-01-01T00:00:00",
            "updated_at": "2025-01-01T00:00:00"
        })

        assert result["$id"] == "test_id_123"
        assert result["name"] == "Test Project"
        mock_post.assert_called_once()

    @patch('app.services.appwrite_service.requests.post')
    def test_create_project_filters_none_values(self, mock_post):
        """Test that None values are filtered out"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"$id": "test_id"}
        mock_post.return_value = mock_response

        service = AppwriteService()
        service.create_project("user123", {
            "name": "Test",
            "repository_url": None,
            "demo_url": None,
            "created_at": "2025-01-01T00:00:00",
            "updated_at": "2025-01-01T00:00:00"
        })

        # Check that None values were filtered out
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        assert "repository_url" not in payload["data"]
        assert "demo_url" not in payload["data"]
        assert "name" in payload["data"]

    @patch('app.services.appwrite_service.requests.get')
    def test_get_projects_success(self, mock_get):
        """Test getting projects successfully"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "documents": [
                {"$id": "1", "name": "Project 1"},
                {"$id": "2", "name": "Project 2"}
            ]
        }
        mock_get.return_value = mock_response

        service = AppwriteService()
        result = service.get_projects("user123")

        assert len(result) == 2
        assert result[0]["name"] == "Project 1"
        mock_get.assert_called_once()

    @patch('app.services.appwrite_service.requests.get')
    def test_get_project_success(self, mock_get):
        """Test getting a single project"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "$id": "project123",
            "name": "Test Project"
        }
        mock_get.return_value = mock_response

        service = AppwriteService()
        result = service.get_project("project123")

        assert result["$id"] == "project123"
        assert result["name"] == "Test Project"

    @patch('app.services.appwrite_service.requests.patch')
    def test_update_project_success(self, mock_patch):
        """Test updating a project"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "$id": "project123",
            "name": "Updated Project"
        }
        mock_patch.return_value = mock_response

        service = AppwriteService()
        result = service.update_project("project123", {
            "name": "Updated Project",
            "updated_at": "2025-01-02T00:00:00"
        })

        assert result["name"] == "Updated Project"
        mock_patch.assert_called_once()

    @patch('app.services.appwrite_service.requests.delete')
    def test_delete_project_success(self, mock_delete):
        """Test deleting a project"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        service = AppwriteService()
        result = service.delete_project("project123")

        assert result is True
        mock_delete.assert_called_once()

    @patch('app.services.appwrite_service.requests.post')
    @patch('app.services.appwrite_service.ID.unique')
    def test_create_build_log_success(self, mock_id, mock_post):
        """Test creating a build log"""
        mock_id.return_value = "log_id_123"
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "$id": "log_id_123",
            "title": "Test Log",
            "project_id": "project123"
        }
        mock_post.return_value = mock_response

        service = AppwriteService()
        result = service.create_build_log("project123", {
            "title": "Test Log",
            "content": "Test content",
            "created_at": "2025-01-01T00:00:00"
        })

        assert result["$id"] == "log_id_123"
        assert result["project_id"] == "project123"

    @patch('app.services.appwrite_service.requests.get')
    def test_get_build_logs_success(self, mock_get):
        """Test getting build logs for a project"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "documents": [
                {"$id": "1", "title": "Log 1", "project_id": "project123"},
                {"$id": "2", "title": "Log 2", "project_id": "project123"},
                {"$id": "3", "title": "Log 3", "project_id": "other_project"}
            ]
        }
        mock_get.return_value = mock_response

        service = AppwriteService()
        result = service.get_build_logs("project123")

        # Should filter to only logs for project123
        assert len(result) == 2
        assert all(log["project_id"] == "project123" for log in result)

    @patch('app.services.appwrite_service.requests.patch')
    def test_update_build_log_success(self, mock_patch):
        """Test updating a build log"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "$id": "log123",
            "title": "Updated Log"
        }
        mock_patch.return_value = mock_response

        service = AppwriteService()
        result = service.update_build_log("log123", {
            "title": "Updated Log"
        })

        assert result["title"] == "Updated Log"

    @patch('app.services.appwrite_service.requests.delete')
    def test_delete_build_log_success(self, mock_delete):
        """Test deleting a build log"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        service = AppwriteService()
        result = service.delete_build_log("log123")

        assert result is True

    @patch('app.services.appwrite_service.requests.post')
    @patch('app.services.appwrite_service.ID.unique')
    def test_upload_file_success(self, mock_id, mock_post):
        """Test file upload"""
        mock_id.return_value = "file_id_123"
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "$id": "file_id_123",
            "name": "test.jpg"
        }
        mock_post.return_value = mock_response

        service = AppwriteService()
        result = service.upload_file(b"file_content", "test.jpg")

        assert result["$id"] == "file_id_123"
        assert result["name"] == "test.jpg"

    def test_get_file_url(self):
        """Test getting file URL"""
        service = AppwriteService()
        url = service.get_file_url("file123")

        assert "file123" in url
        assert "test_storage" in url
        assert "view" in url

    @patch('app.services.appwrite_service.requests.delete')
    def test_delete_file_success(self, mock_delete):
        """Test deleting a file"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        service = AppwriteService()
        result = service.delete_file("file123")

        assert result is True

    @patch('app.services.appwrite_service.requests.post')
    def test_create_project_error_handling(self, mock_post):
        """Test error handling in create_project"""
        mock_post.side_effect = Exception("Network error")

        service = AppwriteService()
        with pytest.raises(Exception) as exc_info:
            service.create_project("user123", {"name": "Test"})

        assert "Network error" in str(exc_info.value)

    @patch('app.services.appwrite_service.requests.get')
    def test_get_projects_error_handling(self, mock_get):
        """Test error handling in get_projects"""
        mock_get.side_effect = Exception("API error")

        service = AppwriteService()
        with pytest.raises(Exception) as exc_info:
            service.get_projects("user123")

        assert "API error" in str(exc_info.value)

    def test_singleton_instance(self):
        """Test that appwrite_service is a singleton instance"""
        assert appwrite_service is not None
        assert isinstance(appwrite_service, AppwriteService)

    @patch('app.services.appwrite_service.requests.patch')
    def test_update_project_filters_none(self, mock_patch):
        """Test that update_project filters None values"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"$id": "project123"}
        mock_patch.return_value = mock_response

        service = AppwriteService()
        service.update_project("project123", {
            "name": "Updated",
            "repository_url": None,
            "demo_url": None
        })

        call_args = mock_patch.call_args
        payload = call_args[1]['json']
        assert "repository_url" not in payload["data"]
        assert "demo_url" not in payload["data"]
        assert "name" in payload["data"]

    @patch('app.services.appwrite_service.requests.get')
    def test_get_project_error_handling(self, mock_get):
        """Test error handling in get_project"""
        mock_get.side_effect = Exception("Connection error")

        service = AppwriteService()
        with pytest.raises(Exception) as exc_info:
            service.get_project("project123")

        assert "Connection error" in str(exc_info.value)

    @patch('app.services.appwrite_service.requests.patch')
    def test_update_project_error_handling(self, mock_patch):
        """Test error handling in update_project"""
        mock_patch.side_effect = Exception("Update failed")

        service = AppwriteService()
        with pytest.raises(Exception) as exc_info:
            service.update_project("project123", {"name": "Test"})

        assert "Update failed" in str(exc_info.value)

    @patch('app.services.appwrite_service.requests.delete')
    def test_delete_project_error_handling(self, mock_delete):
        """Test error handling in delete_project"""
        mock_delete.side_effect = Exception("Delete failed")

        service = AppwriteService()
        with pytest.raises(Exception) as exc_info:
            service.delete_project("project123")

        assert "Delete failed" in str(exc_info.value)

    @patch('app.services.appwrite_service.requests.post')
    def test_create_build_log_error_handling(self, mock_post):
        """Test error handling in create_build_log"""
        mock_post.side_effect = Exception("Create log failed")

        service = AppwriteService()
        with pytest.raises(Exception) as exc_info:
            service.create_build_log("project123", {"title": "Test"})

        assert "Create log failed" in str(exc_info.value)

    @patch('app.services.appwrite_service.requests.get')
    def test_get_build_logs_error_handling(self, mock_get):
        """Test error handling in get_build_logs"""
        mock_get.side_effect = Exception("Fetch logs failed")

        service = AppwriteService()
        with pytest.raises(Exception) as exc_info:
            service.get_build_logs("project123")

        assert "Fetch logs failed" in str(exc_info.value)

    @patch('app.services.appwrite_service.requests.patch')
    def test_update_build_log_error_handling(self, mock_patch):
        """Test error handling in update_build_log"""
        mock_patch.side_effect = Exception("Update log failed")

        service = AppwriteService()
        with pytest.raises(Exception) as exc_info:
            service.update_build_log("log123", {"title": "Updated"})

        assert "Update log failed" in str(exc_info.value)

    @patch('app.services.appwrite_service.requests.delete')
    def test_delete_build_log_error_handling(self, mock_delete):
        """Test error handling in delete_build_log"""
        mock_delete.side_effect = Exception("Delete log failed")

        service = AppwriteService()
        with pytest.raises(Exception) as exc_info:
            service.delete_build_log("log123")

        assert "Delete log failed" in str(exc_info.value)

    @patch('app.services.appwrite_service.requests.post')
    def test_upload_file_error_handling(self, mock_post):
        """Test error handling in upload_file"""
        mock_post.side_effect = Exception("Upload failed")

        service = AppwriteService()
        with pytest.raises(Exception) as exc_info:
            service.upload_file(b"content", "test.jpg")

        assert "Upload failed" in str(exc_info.value)

    @patch('app.services.appwrite_service.requests.delete')
    def test_delete_file_error_handling(self, mock_delete):
        """Test error handling in delete_file"""
        mock_delete.side_effect = Exception("Delete file failed")

        service = AppwriteService()
        with pytest.raises(Exception) as exc_info:
            service.delete_file("file123")

        assert "Delete file failed" in str(exc_info.value)
