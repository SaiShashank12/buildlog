"""
Unit tests for Pydantic models and schemas
"""
import pytest
from pydantic import ValidationError
from app.models.schemas import (
    ProjectCreate, ProjectUpdate, BuildLogCreate, BuildLogUpdate,
    UserLogin, UserRegister, MarkdownExportRequest, AIGenerateRequest
)


class TestProjectCreate:
    """Test ProjectCreate schema"""

    def test_valid_project_create(self):
        """Test creating a valid project"""
        project = ProjectCreate(
            name="Test Project",
            description="A test project",
            tech_stack=["Python", "FastAPI"],
            repository_url="https://github.com/user/repo",
            demo_url="https://demo.com",
            tags=["test", "demo"]
        )
        assert project.name == "Test Project"
        assert project.description == "A test project"
        assert len(project.tech_stack) == 2
        assert project.repository_url == "https://github.com/user/repo"

    def test_project_create_minimal(self):
        """Test creating project with minimal required fields"""
        project = ProjectCreate(name="Minimal Project")
        assert project.name == "Minimal Project"
        assert project.description is None
        assert project.tech_stack == []

    def test_project_create_empty_name_fails(self):
        """Test that empty name fails validation"""
        with pytest.raises(ValidationError):
            ProjectCreate(name="")

    def test_project_create_long_name_fails(self):
        """Test that name longer than 200 chars fails"""
        with pytest.raises(ValidationError):
            ProjectCreate(name="a" * 201)


class TestProjectUpdate:
    """Test ProjectUpdate schema"""

    def test_valid_project_update(self):
        """Test updating project with valid data"""
        update = ProjectUpdate(
            name="Updated Project",
            status="completed"
        )
        assert update.name == "Updated Project"
        assert update.status == "completed"

    def test_project_update_all_optional(self):
        """Test that all fields are optional in update"""
        update = ProjectUpdate()
        assert update.name is None
        assert update.description is None
        assert update.tech_stack is None


class TestBuildLogCreate:
    """Test BuildLogCreate schema"""

    def test_valid_build_log_create(self):
        """Test creating a valid build log"""
        log = BuildLogCreate(
            title="Test Log",
            content="This is a test log entry",
            log_type="milestone",
            tags=["test"]
        )
        assert log.title == "Test Log"
        assert log.content == "This is a test log entry"
        assert log.log_type == "milestone"
        assert log.tags == ["test"]

    def test_build_log_create_default_type(self):
        """Test that log_type defaults to 'update'"""
        log = BuildLogCreate(
            title="Test",
            content="Content"
        )
        assert log.log_type == "update"

    def test_build_log_create_empty_title_fails(self):
        """Test that empty title fails validation"""
        with pytest.raises(ValidationError):
            BuildLogCreate(title="", content="Content")

    def test_build_log_create_empty_content_fails(self):
        """Test that empty content fails validation"""
        with pytest.raises(ValidationError):
            BuildLogCreate(title="Title", content="")

    def test_build_log_create_with_arrays(self):
        """Test build log with code snippets, images, and links"""
        log = BuildLogCreate(
            title="Feature Complete",
            content="Implemented new feature",
            code_snippets=[{"language": "python", "code": "print('hello')"}],
            images=["img1.jpg", "img2.jpg"],
            links=[{"title": "GitHub", "url": "https://github.com"}]
        )
        assert len(log.code_snippets) == 1
        assert len(log.images) == 2
        assert len(log.links) == 1


class TestBuildLogUpdate:
    """Test BuildLogUpdate schema"""

    def test_build_log_update_partial(self):
        """Test partial update of build log"""
        update = BuildLogUpdate(title="Updated Title")
        assert update.title == "Updated Title"
        assert update.content is None

    def test_build_log_update_all_optional(self):
        """Test that all fields are optional"""
        update = BuildLogUpdate()
        assert update.title is None
        assert update.content is None


class TestUserLogin:
    """Test UserLogin schema"""

    def test_valid_user_login(self):
        """Test valid user login data"""
        login = UserLogin(
            email="test@example.com",
            password="securepassword123"
        )
        assert login.email == "test@example.com"
        assert login.password == "securepassword123"

    def test_user_login_requires_fields(self):
        """Test that email and password are required"""
        with pytest.raises(ValidationError):
            UserLogin(email="test@example.com")


class TestUserRegister:
    """Test UserRegister schema"""

    def test_valid_user_register(self):
        """Test valid user registration data"""
        register = UserRegister(
            email="test@example.com",
            password="securepassword123",
            name="Test User"
        )
        assert register.email == "test@example.com"
        assert register.password == "securepassword123"
        assert register.name == "Test User"


class TestMarkdownExportRequest:
    """Test MarkdownExportRequest schema"""

    def test_valid_export_request(self):
        """Test valid markdown export request"""
        request = MarkdownExportRequest(
            project_id="123",
            include_logs=True,
            include_images=True,
            include_code_snippets=True
        )
        assert request.project_id == "123"
        assert request.include_logs is True

    def test_export_request_defaults(self):
        """Test default values in export request"""
        request = MarkdownExportRequest(project_id="123")
        assert request.include_logs is True
        assert request.include_images is True
        assert request.include_code_snippets is True


class TestAIGenerateRequest:
    """Test AIGenerateRequest schema"""

    def test_valid_ai_generate_request(self):
        """Test valid AI generation request"""
        request = AIGenerateRequest(
            prompt="Write a description",
            context="Project context",
            max_length=300
        )
        assert request.prompt == "Write a description"
        assert request.context == "Project context"
        assert request.max_length == 300

    def test_ai_generate_default_max_length(self):
        """Test default max_length"""
        request = AIGenerateRequest(prompt="Test prompt")
        assert request.max_length == 500

    def test_ai_generate_empty_prompt_fails(self):
        """Test that empty prompt fails validation"""
        with pytest.raises(ValidationError):
            AIGenerateRequest(prompt="")
