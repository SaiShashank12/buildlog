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
        # Mock synchronous methods (no longer async)
        mock.get_projects = Mock(return_value=[])
        mock.get_project = Mock(return_value={
            '$id': '123',
            'name': 'Test Project',
            'description': 'Test description',
            'tech_stack': ['Python'],
            'status': 'in_progress'
        })
        mock.create_project = Mock(return_value={
            '$id': '123',
            'name': 'New Project'
        })
        mock.update_project = Mock(return_value={
            '$id': '123',
            'name': 'Updated Project'
        })
        mock.delete_project = Mock(return_value=True)
        mock.get_build_logs = Mock(return_value=[])
        mock.create_build_log = Mock(return_value={
            '$id': 'log123',
            'title': 'New Log'
        })
        mock.update_build_log = Mock(return_value={
            '$id': 'log123',
            'title': 'Updated Log'
        })
        mock.delete_build_log = Mock(return_value=True)
        mock.upload_file = Mock(return_value={
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

    def test_dashboard_error_handling(self, client, mock_appwrite):
        """Test dashboard handles errors gracefully"""
        mock_appwrite.get_projects.side_effect = Exception("Database error")
        response = client.get("/dashboard")
        # Should return dashboard with empty projects
        assert response.status_code == 200
        assert "Dashboard" in response.text

    def test_create_project_error_handling(self, client, mock_appwrite):
        """Test create project error handling"""
        mock_appwrite.create_project.side_effect = Exception("Database error")
        response = client.post(
            "/projects/new",
            data={
                "name": "Test Project",
                "description": "Test description"
            },
            follow_redirects=False
        )
        assert response.status_code == 500

    def test_edit_project_not_found(self, client, mock_appwrite):
        """Test editing nonexistent project"""
        mock_appwrite.get_project.side_effect = Exception("Not found")
        response = client.get("/projects/999/edit")
        assert response.status_code == 404

    def test_update_project_error_handling(self, client, mock_appwrite):
        """Test update project error handling"""
        mock_appwrite.update_project.side_effect = Exception("Update error")
        response = client.post(
            "/projects/123/edit",
            data={
                "name": "Updated Project",
                "description": "Updated"
            },
            follow_redirects=False
        )
        assert response.status_code == 500

    def test_delete_project_error_handling(self, client, mock_appwrite):
        """Test delete project error handling"""
        mock_appwrite.delete_project.side_effect = Exception("Delete error")
        response = client.post("/projects/123/delete", follow_redirects=False)
        assert response.status_code == 500

    def test_new_log_form_error_handling(self, client, mock_appwrite):
        """Test new log form with nonexistent project"""
        mock_appwrite.get_project.side_effect = Exception("Not found")
        response = client.get("/projects/999/logs/new")
        assert response.status_code == 404

    def test_create_build_log_error_handling(self, client, mock_appwrite):
        """Test create build log error handling"""
        mock_appwrite.create_build_log.side_effect = Exception("Create error")
        response = client.post(
            "/projects/123/logs/new",
            data={
                "title": "Test Log",
                "content": "Content"
            },
            follow_redirects=False
        )
        assert response.status_code == 500

    def test_edit_log_not_found(self, client, mock_appwrite):
        """Test editing nonexistent log"""
        mock_appwrite.get_project.return_value = {"$id": "123", "name": "Project"}
        mock_appwrite.get_build_logs.return_value = []
        response = client.get("/projects/123/logs/999/edit")
        assert response.status_code == 404

    def test_edit_log_project_not_found(self, client, mock_appwrite):
        """Test editing log when project not found"""
        mock_appwrite.get_project.side_effect = Exception("Not found")
        response = client.get("/projects/123/logs/log123/edit")
        assert response.status_code == 404

    def test_update_build_log_error_handling(self, client, mock_appwrite):
        """Test update build log error handling"""
        mock_appwrite.update_build_log.side_effect = Exception("Update error")
        response = client.post(
            "/projects/123/logs/log123/edit",
            data={
                "title": "Updated Log",
                "content": "Updated content"
            },
            follow_redirects=False
        )
        assert response.status_code == 500

    def test_delete_build_log_error_handling(self, client, mock_appwrite):
        """Test delete build log error handling"""
        mock_appwrite.delete_build_log.side_effect = Exception("Delete error")
        response = client.post("/projects/123/logs/log123/delete", follow_redirects=False)
        assert response.status_code == 500

    def test_export_error_handling(self, client, mock_appwrite):
        """Test export error handling"""
        mock_appwrite.get_project.side_effect = Exception("Not found")
        response = client.get("/projects/123/export")
        assert response.status_code == 500

    def test_portfolio_error_handling(self, client, mock_appwrite):
        """Test portfolio error handling"""
        mock_appwrite.get_project.side_effect = Exception("Not found")
        response = client.get("/portfolio/123")
        assert response.status_code == 404

    def test_upload_file_error_handling(self, client, mock_appwrite):
        """Test upload file error handling"""
        from io import BytesIO
        mock_appwrite.upload_file.side_effect = Exception("Upload error")

        file_data = BytesIO(b"fake image data")
        response = client.post(
            "/upload",
            files={"file": ("test.jpg", file_data, "image/jpeg")}
        )
        assert response.status_code == 500


class TestAIEndpoints:
    """Test AI-powered endpoints"""

    @patch('main.ai_service')
    def test_ai_status_enabled(self, mock_ai_service, client):
        """Test AI status endpoint when AI is enabled"""
        mock_ai_service.is_enabled.return_value = True
        response = client.get("/ai/status")
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["enabled"] is True

    @patch('main.ai_service')
    def test_ai_status_disabled(self, mock_ai_service, client):
        """Test AI status endpoint when AI is disabled"""
        mock_ai_service.is_enabled.return_value = False
        response = client.get("/ai/status")
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["enabled"] is False

    @patch('main.ai_service')
    def test_generate_description_success(self, mock_ai_service, client):
        """Test successful AI description generation"""
        mock_ai_service.is_enabled.return_value = True
        mock_ai_service.generate_project_description.return_value = "AI generated description"

        response = client.post(
            "/ai/generate-description",
            data={
                "project_name": "Test Project",
                "tech_stack": "Python,FastAPI"
            }
        )
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["success"] is True
        assert json_response["description"] == "AI generated description"

    @patch('main.ai_service')
    def test_generate_description_ai_disabled(self, mock_ai_service, client):
        """Test AI description generation when AI is disabled"""
        mock_ai_service.is_enabled.return_value = False

        response = client.post(
            "/ai/generate-description",
            data={
                "project_name": "Test Project",
                "tech_stack": "Python"
            }
        )
        assert response.status_code == 400
        json_response = response.json()
        assert json_response["success"] is False
        assert "not enabled" in json_response["error"]

    @patch('main.ai_service')
    def test_generate_description_empty_result(self, mock_ai_service, client):
        """Test AI description generation with empty result"""
        mock_ai_service.is_enabled.return_value = True
        mock_ai_service.generate_project_description.return_value = ""

        response = client.post(
            "/ai/generate-description",
            data={
                "project_name": "Test Project",
                "tech_stack": ""
            }
        )
        assert response.status_code == 500
        json_response = response.json()
        assert json_response["success"] is False

    @patch('main.ai_service')
    def test_generate_log_content_success(self, mock_ai_service, client):
        """Test successful AI log content generation"""
        mock_ai_service.is_enabled.return_value = True
        mock_ai_service.generate_build_log_content.return_value = "AI generated log content"

        response = client.post(
            "/ai/generate-log-content",
            data={
                "project_name": "Test Project",
                "log_type": "milestone",
                "context": "Big achievement"
            }
        )
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["success"] is True
        assert json_response["content"] == "AI generated log content"

    @patch('main.ai_service')
    def test_generate_log_content_ai_disabled(self, mock_ai_service, client):
        """Test AI log content generation when AI is disabled"""
        mock_ai_service.is_enabled.return_value = False

        response = client.post(
            "/ai/generate-log-content",
            data={
                "project_name": "Test Project",
                "log_type": "update",
                "context": ""
            }
        )
        assert response.status_code == 400
        json_response = response.json()
        assert json_response["success"] is False
        assert "not enabled" in json_response["error"]

    @patch('main.ai_service')
    def test_generate_log_content_empty_result(self, mock_ai_service, client):
        """Test AI log content generation with empty result"""
        mock_ai_service.is_enabled.return_value = True
        mock_ai_service.generate_build_log_content.return_value = ""

        response = client.post(
            "/ai/generate-log-content",
            data={
                "project_name": "Test Project",
                "log_type": "feature",
                "context": ""
            }
        )
        assert response.status_code == 500
        json_response = response.json()
        assert json_response["success"] is False

    @patch('main.ai_service')
    def test_generate_log_content_all_types(self, mock_ai_service, client):
        """Test AI log content generation for all log types"""
        mock_ai_service.is_enabled.return_value = True
        mock_ai_service.generate_build_log_content.return_value = "Generated content"

        for log_type in ["update", "milestone", "feature", "bug_fix", "note"]:
            response = client.post(
                "/ai/generate-log-content",
                data={
                    "project_name": "Test",
                    "log_type": log_type,
                    "context": ""
                }
            )
            assert response.status_code == 200
            json_response = response.json()
            assert json_response["success"] is True


class TestAnalyticsEndpoints:
    """Test analytics dashboard and API endpoints"""

    def test_analytics_dashboard_page(self, client):
        """Test analytics dashboard page loads"""
        response = client.get("/analytics")
        assert response.status_code == 200
        assert "Analytics" in response.text or "Chart" in response.text

    @patch('main.analytics_service')
    def test_get_analytics_data(self, mock_analytics, client, mock_appwrite):
        """Test getting analytics data"""
        mock_analytics.get_complete_analytics.return_value = {
            'total_projects': 5,
            'total_logs': 20,
            'active_projects': 3,
            'weekly_logs': 7,
            'activity_over_time': {
                'labels': ['Jan 1', 'Jan 2', 'Jan 3'],
                'values': [5, 8, 3]
            },
            'log_type_distribution': {
                'labels': ['Update', 'Milestone', 'Feature'],
                'values': [10, 5, 5]
            },
            'logs_per_project': {
                'labels': ['Project 1', 'Project 2'],
                'values': [12, 8]
            },
            'weekly_trend': {
                'labels': ['Week 1', 'Week 2'],
                'values': [10, 10]
            },
            'activity_heatmap': [
                {'date': '2024-01-01', 'count': 2},
                {'date': '2024-01-02', 'count': 3}
            ],
            'project_status': {
                'labels': ['In Progress', 'Completed'],
                'values': [3, 2]
            }
        }

        response = client.get("/api/analytics")
        assert response.status_code == 200
        json_response = response.json()

        # Check all required fields
        assert 'total_projects' in json_response
        assert 'total_logs' in json_response
        assert 'active_projects' in json_response
        assert 'weekly_logs' in json_response
        assert 'activity_over_time' in json_response
        assert 'log_type_distribution' in json_response
        assert 'logs_per_project' in json_response
        assert 'weekly_trend' in json_response
        assert 'activity_heatmap' in json_response
        assert 'project_status' in json_response

        # Verify data values
        assert json_response['total_projects'] == 5
        assert json_response['total_logs'] == 20
        assert json_response['active_projects'] == 3

    @patch('main.analytics_service')
    def test_get_analytics_with_no_data(self, mock_analytics, client, mock_appwrite):
        """Test analytics with no data"""
        mock_analytics.get_complete_analytics.return_value = {
            'total_projects': 0,
            'total_logs': 0,
            'active_projects': 0,
            'weekly_logs': 0,
            'activity_over_time': {'labels': [], 'values': []},
            'log_type_distribution': {'labels': [], 'values': []},
            'logs_per_project': {'labels': [], 'values': []},
            'weekly_trend': {'labels': [], 'values': []},
            'activity_heatmap': [],
            'project_status': {'labels': [], 'values': []}
        }

        response = client.get("/api/analytics")
        assert response.status_code == 200
        json_response = response.json()
        assert json_response['total_projects'] == 0
        assert json_response['total_logs'] == 0

    @patch('main.analytics_service')
    def test_analytics_error_handling(self, mock_analytics, client, mock_appwrite):
        """Test analytics API error handling"""
        mock_analytics.get_complete_analytics.side_effect = Exception("Analytics error")

        response = client.get("/api/analytics")
        assert response.status_code == 500
        json_response = response.json()
        assert "error" in json_response

    def test_analytics_dashboard_error_handling(self, client, mock_appwrite):
        """Test analytics dashboard handles errors gracefully"""
        response = client.get("/analytics")
        # Should still return the page even if data fails to load
        assert response.status_code == 200
