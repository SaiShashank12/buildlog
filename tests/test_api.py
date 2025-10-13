"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, AsyncMock
from main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def mock_appwrite():
    """Mock Appwrite service"""
    with patch('main.appwrite_service') as mock:
        # Mock async methods
        mock.get_projects = AsyncMock(return_value=[])
        mock.get_project = AsyncMock(return_value={
            '$id': '123',
            'name': 'Test Project',
            'description': 'Test description',
            'tech_stack': ['Python'],
            'status': 'in_progress'
        })
        mock.create_project = AsyncMock(return_value={
            '$id': '123',
            'name': 'New Project'
        })
        mock.update_project = AsyncMock(return_value={
            '$id': '123',
            'name': 'Updated Project'
        })
        mock.delete_project = AsyncMock(return_value=True)
        mock.get_build_logs = AsyncMock(return_value=[])
        mock.create_build_log = AsyncMock(return_value={
            '$id': 'log123',
            'title': 'New Log'
        })
        mock.update_build_log = AsyncMock(return_value={
            '$id': 'log123',
            'title': 'Updated Log'
        })
        mock.delete_build_log = AsyncMock(return_value=True)
        mock.upload_file = AsyncMock(return_value={
            '$id': 'file123',
            'name': 'test.jpg'
        })
        yield mock


class TestHomeEndpoint:
    """Test homepage endpoint"""

    def test_home_returns_200(self, client):
        """Test that homepage returns 200 OK"""
        response = client.get("/")
        assert response.status_code == 200
        assert "BuildLog" in response.text

    def test_home_contains_title(self, client):
        """Test that homepage contains expected title"""
        response = client.get("/")
        assert "Document Your Journey" in response.text or "BuildLog" in response.text


class TestDashboardEndpoint:
    """Test dashboard endpoint"""

    def test_dashboard_returns_200(self, client, mock_appwrite):
        """Test dashboard returns 200 OK"""
        response = client.get("/dashboard")
        assert response.status_code == 200

    def test_dashboard_with_projects(self, client, mock_appwrite):
        """Test dashboard with projects"""
        mock_appwrite.get_projects.return_value = [
            {'$id': '1', 'name': 'Project 1', 'status': 'in_progress', 'created_at': '2025-10-13'},
            {'$id': '2', 'name': 'Project 2', 'status': 'completed', 'created_at': '2025-10-12'}
        ]
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert "Project 1" in response.text or "Dashboard" in response.text


class TestProjectEndpoints:
    """Test project-related endpoints"""

    def test_new_project_form(self, client):
        """Test new project form page"""
        response = client.get("/projects/new")
        assert response.status_code == 200
        assert "Create" in response.text or "Project" in response.text

    def test_create_project(self, client, mock_appwrite):
        """Test creating a new project"""
        response = client.post(
            "/projects/new",
            data={
                "name": "Test Project",
                "description": "Test description",
                "tech_stack": "Python,FastAPI",
                "repository_url": "https://github.com/test/repo",
                "demo_url": "https://demo.test.com",
                "tags": "test,demo"
            },
            follow_redirects=False
        )
        assert response.status_code in [200, 303]

    def test_view_project(self, client, mock_appwrite):
        """Test viewing a single project"""
        response = client.get("/projects/123")
        assert response.status_code == 200

    def test_edit_project_form(self, client, mock_appwrite):
        """Test edit project form"""
        response = client.get("/projects/123/edit")
        assert response.status_code == 200

    def test_update_project(self, client, mock_appwrite):
        """Test updating a project"""
        response = client.post(
            "/projects/123/edit",
            data={
                "name": "Updated Project",
                "description": "Updated description",
                "tech_stack": "Python",
                "repository_url": "",
                "demo_url": "",
                "tags": "",
                "status": "completed"
            },
            follow_redirects=False
        )
        assert response.status_code in [200, 303]

    def test_delete_project(self, client, mock_appwrite):
        """Test deleting a project"""
        response = client.post("/projects/123/delete", follow_redirects=False)
        assert response.status_code in [200, 303]

    def test_view_nonexistent_project(self, client, mock_appwrite):
        """Test viewing nonexistent project returns 404"""
        mock_appwrite.get_project.side_effect = Exception("Not found")
        response = client.get("/projects/nonexistent")
        assert response.status_code == 404


class TestBuildLogEndpoints:
    """Test build log endpoints"""

    def test_new_log_form(self, client, mock_appwrite):
        """Test new build log form"""
        response = client.get("/projects/123/logs/new")
        assert response.status_code == 200

    def test_create_build_log(self, client, mock_appwrite):
        """Test creating a build log"""
        response = client.post(
            "/projects/123/logs/new",
            data={
                "title": "Test Log",
                "content": "Log content here",
                "log_type": "update",
                "tags": "test,log"
            },
            follow_redirects=False
        )
        assert response.status_code in [200, 303]

    def test_edit_log_form(self, client, mock_appwrite):
        """Test edit build log form"""
        mock_appwrite.get_build_logs.return_value = [
            {'$id': 'log123', 'title': 'Test Log', 'content': 'Content'}
        ]
        response = client.get("/projects/123/logs/log123/edit")
        assert response.status_code == 200

    def test_update_build_log(self, client, mock_appwrite):
        """Test updating a build log"""
        response = client.post(
            "/projects/123/logs/log123/edit",
            data={
                "title": "Updated Log",
                "content": "Updated content",
                "log_type": "milestone",
                "tags": "milestone"
            },
            follow_redirects=False
        )
        assert response.status_code in [200, 303]

    def test_delete_build_log(self, client, mock_appwrite):
        """Test deleting a build log"""
        response = client.post("/projects/123/logs/log123/delete", follow_redirects=False)
        assert response.status_code in [200, 303]


class TestExportEndpoint:
    """Test markdown export endpoint"""

    def test_export_to_markdown(self, client, mock_appwrite):
        """Test exporting project to markdown"""
        mock_appwrite.get_build_logs.return_value = [
            {
                '$id': 'log1',
                'title': 'First Log',
                'content': 'Content here',
                'created_at': '2025-10-13',
                'log_type': 'update'
            }
        ]
        response = client.get("/projects/123/export")
        assert response.status_code == 200
        assert "markdown" in response.text.lower() or "export" in response.text.lower()


class TestPortfolioEndpoint:
    """Test public portfolio endpoint"""

    def test_public_portfolio(self, client, mock_appwrite):
        """Test public portfolio page"""
        mock_appwrite.get_build_logs.return_value = [
            {
                '$id': 'log1',
                'title': 'Milestone',
                'content': 'Achieved milestone',
                'created_at': '2025-10-13',
                'log_type': 'milestone',
                'tags': []
            }
        ]
        response = client.get("/portfolio/123")
        assert response.status_code == 200


class TestFileUploadEndpoint:
    """Test file upload endpoint"""

    def test_upload_file(self, client, mock_appwrite):
        """Test uploading a file"""
        from io import BytesIO

        file_data = BytesIO(b"fake image data")
        response = client.post(
            "/upload",
            files={"file": ("test.jpg", file_data, "image/jpeg")}
        )
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["success"] is True
        assert "file_id" in json_response


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check(self, client):
        """Test health check returns 200 and correct status"""
        response = client.get("/health")
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["status"] == "healthy"
        assert json_response["service"] == "BuildLog API"


class TestErrorHandling:
    """Test error handling"""

    def test_404_error(self, client):
        """Test that 404 is returned for nonexistent routes"""
        response = client.get("/nonexistent/route")
        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """Test that wrong HTTP methods are rejected"""
        response = client.put("/")
        assert response.status_code == 405

    def test_create_project_missing_name(self, client, mock_appwrite):
        """Test creating project without required name field"""
        response = client.post(
            "/projects/new",
            data={
                "description": "Test description"
            },
            follow_redirects=False
        )
        # Should either return error or validation error
        assert response.status_code in [400, 422, 500]

    def test_create_log_missing_required_fields(self, client, mock_appwrite):
        """Test creating log without required fields"""
        response = client.post(
            "/projects/123/logs/new",
            data={
                "log_type": "update"
            },
            follow_redirects=False
        )
        # Should return error for missing required fields
        assert response.status_code in [400, 422, 500]
