"""
Unit tests for Appwrite service layer
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.appwrite_service import AppwriteService


class TestAppwriteService:
    """Test AppwriteService class"""

    @pytest.fixture
    def mock_appwrite_service(self):
        """Create mock Appwrite service"""
        with patch('app.services.appwrite_service.Client') as mock_client, \
             patch('app.services.appwrite_service.Databases') as mock_db, \
             patch('app.services.appwrite_service.Storage') as mock_storage, \
             patch('app.services.appwrite_service.Account') as mock_account, \
             patch('app.services.appwrite_service.Users') as mock_users:

            service = AppwriteService()
            service.databases = mock_db.return_value
            service.storage = mock_storage.return_value
            service.account = mock_account.return_value
            service.users = mock_users.return_value

            return service

    @pytest.mark.asyncio
    async def test_create_project(self, mock_appwrite_service):
        """Test creating a project"""
        mock_appwrite_service.databases.create_document = Mock(return_value={
            '$id': '123',
            'name': 'Test Project',
            'user_id': 'user123'
        })

        result = await mock_appwrite_service.create_project(
            user_id='user123',
            data={
                'name': 'Test Project',
                'description': 'Test description',
                'created_at': '2025-10-13',
                'updated_at': '2025-10-13'
            }
        )

        assert result['$id'] == '123'
        assert result['name'] == 'Test Project'
        mock_appwrite_service.databases.create_document.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_projects(self, mock_appwrite_service):
        """Test getting all projects for a user"""
        mock_appwrite_service.databases.list_documents = Mock(return_value={
            'documents': [
                {'$id': '1', 'name': 'Project 1'},
                {'$id': '2', 'name': 'Project 2'}
            ]
        })

        result = await mock_appwrite_service.get_projects(user_id='user123')

        assert len(result) == 2
        assert result[0]['name'] == 'Project 1'
        mock_appwrite_service.databases.list_documents.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_project(self, mock_appwrite_service):
        """Test getting a single project"""
        mock_appwrite_service.databases.get_document = Mock(return_value={
            '$id': '123',
            'name': 'Test Project'
        })

        result = await mock_appwrite_service.get_project(project_id='123')

        assert result['$id'] == '123'
        assert result['name'] == 'Test Project'
        mock_appwrite_service.databases.get_document.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_project(self, mock_appwrite_service):
        """Test updating a project"""
        mock_appwrite_service.databases.update_document = Mock(return_value={
            '$id': '123',
            'name': 'Updated Project'
        })

        result = await mock_appwrite_service.update_project(
            project_id='123',
            data={'name': 'Updated Project'}
        )

        assert result['name'] == 'Updated Project'
        mock_appwrite_service.databases.update_document.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_project(self, mock_appwrite_service):
        """Test deleting a project"""
        mock_appwrite_service.databases.delete_document = Mock(return_value=None)

        result = await mock_appwrite_service.delete_project(project_id='123')

        assert result is True
        mock_appwrite_service.databases.delete_document.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_build_log(self, mock_appwrite_service):
        """Test creating a build log"""
        mock_appwrite_service.databases.create_document = Mock(return_value={
            '$id': 'log123',
            'title': 'Test Log',
            'project_id': '123'
        })

        result = await mock_appwrite_service.create_build_log(
            project_id='123',
            data={
                'title': 'Test Log',
                'content': 'Log content',
                'created_at': '2025-10-13'
            }
        )

        assert result['$id'] == 'log123'
        assert result['title'] == 'Test Log'
        mock_appwrite_service.databases.create_document.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_build_logs(self, mock_appwrite_service):
        """Test getting build logs for a project"""
        mock_appwrite_service.databases.list_documents = Mock(return_value={
            'documents': [
                {'$id': 'log1', 'title': 'Log 1'},
                {'$id': 'log2', 'title': 'Log 2'}
            ]
        })

        result = await mock_appwrite_service.get_build_logs(project_id='123')

        assert len(result) == 2
        assert result[0]['title'] == 'Log 1'
        mock_appwrite_service.databases.list_documents.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_build_log(self, mock_appwrite_service):
        """Test updating a build log"""
        mock_appwrite_service.databases.update_document = Mock(return_value={
            '$id': 'log123',
            'title': 'Updated Log'
        })

        result = await mock_appwrite_service.update_build_log(
            log_id='log123',
            data={'title': 'Updated Log'}
        )

        assert result['title'] == 'Updated Log'
        mock_appwrite_service.databases.update_document.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_build_log(self, mock_appwrite_service):
        """Test deleting a build log"""
        mock_appwrite_service.databases.delete_document = Mock(return_value=None)

        result = await mock_appwrite_service.delete_build_log(log_id='log123')

        assert result is True
        mock_appwrite_service.databases.delete_document.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload_file(self, mock_appwrite_service):
        """Test uploading a file"""
        mock_appwrite_service.storage.create_file = Mock(return_value={
            '$id': 'file123',
            'name': 'test.jpg'
        })

        result = await mock_appwrite_service.upload_file(
            file_content=b'fake image data',
            file_name='test.jpg'
        )

        assert result['$id'] == 'file123'
        assert result['name'] == 'test.jpg'
        mock_appwrite_service.storage.create_file.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_file_url(self, mock_appwrite_service):
        """Test getting file URL"""
        mock_appwrite_service.storage.get_file_view = Mock(return_value='https://example.com/file123')

        result = await mock_appwrite_service.get_file_url(file_id='file123')

        assert result == 'https://example.com/file123'
        mock_appwrite_service.storage.get_file_view.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_file(self, mock_appwrite_service):
        """Test deleting a file"""
        mock_appwrite_service.storage.delete_file = Mock(return_value=None)

        result = await mock_appwrite_service.delete_file(file_id='file123')

        assert result is True
        mock_appwrite_service.storage.delete_file.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_project_error_handling(self, mock_appwrite_service):
        """Test error handling when creating project fails"""
        mock_appwrite_service.databases.create_document = Mock(
            side_effect=Exception("Database error")
        )

        with pytest.raises(Exception) as exc_info:
            await mock_appwrite_service.create_project(
                user_id='user123',
                data={'name': 'Test', 'created_at': '2025-10-13', 'updated_at': '2025-10-13'}
            )

        assert "Database error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_projects_error_handling(self, mock_appwrite_service):
        """Test error handling when getting projects fails"""
        mock_appwrite_service.databases.list_documents = Mock(
            side_effect=Exception("Query error")
        )

        with pytest.raises(Exception) as exc_info:
            await mock_appwrite_service.get_projects(user_id='user123')

        assert "Query error" in str(exc_info.value)
