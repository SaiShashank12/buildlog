"""
Tests for AI service
"""
import pytest
from unittest.mock import patch, Mock
from app.services.ai_service import AIService


class TestAIService:
    """Test AI service functionality"""

    def test_ai_service_disabled_by_default(self):
        """Test that AI service is disabled without API key"""
        with patch('app.services.ai_service.settings') as mock_settings:
            mock_settings.openai_api_key = ""
            mock_settings.ai_enabled = False
            service = AIService()
            assert service.is_enabled() is False

    def test_ai_service_enabled_with_api_key(self):
        """Test that AI service is enabled with API key"""
        with patch('app.services.ai_service.settings') as mock_settings:
            mock_settings.openai_api_key = "test-key"
            mock_settings.ai_enabled = True
            service = AIService()
            assert service.is_enabled() is True

    @patch('app.services.ai_service.settings')
    def test_generate_project_description_disabled(self, mock_settings):
        """Test generate_project_description when AI is disabled"""
        mock_settings.openai_api_key = ""
        mock_settings.ai_enabled = False
        service = AIService()
        result = service.generate_project_description("Test Project", ["Python", "FastAPI"])
        assert result == ""

    @patch('app.services.ai_service.settings')
    @patch('app.services.ai_service.AIService.is_enabled', return_value=True)
    def test_generate_project_description_success(self, mock_enabled, mock_settings):
        """Test successful project description generation"""
        mock_settings.openai_api_key = "test-key"
        mock_settings.ai_enabled = True

        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "A great project description"
            mock_client.chat.completions.create.return_value = mock_response

            service = AIService()
            result = service.generate_project_description("Test Project", ["Python", "FastAPI"])
            assert result == "A great project description"

    @patch('app.services.ai_service.settings')
    @patch('app.services.ai_service.AIService.is_enabled', return_value=True)
    def test_generate_project_description_error(self, mock_enabled, mock_settings):
        """Test project description generation with error"""
        mock_settings.openai_api_key = "test-key"
        mock_settings.ai_enabled = True

        with patch('openai.OpenAI') as mock_openai:
            mock_openai.side_effect = Exception("API Error")

            service = AIService()
            result = service.generate_project_description("Test Project", ["Python"])
            assert result == ""

    @patch('app.services.ai_service.settings')
    def test_generate_build_log_content_disabled(self, mock_settings):
        """Test generate_build_log_content when AI is disabled"""
        mock_settings.openai_api_key = ""
        mock_settings.ai_enabled = False
        service = AIService()
        result = service.generate_build_log_content("Test Project", "update", "context")
        assert result == ""

    @patch('app.services.ai_service.settings')
    @patch('app.services.ai_service.AIService.is_enabled', return_value=True)
    def test_generate_build_log_content_success(self, mock_enabled, mock_settings):
        """Test successful build log content generation"""
        mock_settings.openai_api_key = "test-key"
        mock_settings.ai_enabled = True

        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Generated log content"
            mock_client.chat.completions.create.return_value = mock_response

            service = AIService()
            result = service.generate_build_log_content("Test Project", "milestone", "Big achievement")
            assert result == "Generated log content"

    @patch('app.services.ai_service.settings')
    @patch('app.services.ai_service.AIService.is_enabled', return_value=True)
    def test_generate_build_log_content_all_types(self, mock_enabled, mock_settings):
        """Test build log content generation for all log types"""
        mock_settings.openai_api_key = "test-key"
        mock_settings.ai_enabled = True

        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Generated content"
            mock_client.chat.completions.create.return_value = mock_response

            service = AIService()

            for log_type in ["update", "milestone", "feature", "bug_fix", "note"]:
                result = service.generate_build_log_content("Test", log_type)
                assert result == "Generated content"

    @patch('app.services.ai_service.settings')
    @patch('app.services.ai_service.AIService.is_enabled', return_value=True)
    def test_generate_build_log_content_error(self, mock_enabled, mock_settings):
        """Test build log content generation with error"""
        mock_settings.openai_api_key = "test-key"
        mock_settings.ai_enabled = True

        with patch('openai.OpenAI') as mock_openai:
            mock_openai.side_effect = Exception("API Error")

            service = AIService()
            result = service.generate_build_log_content("Test Project", "update")
            assert result == ""

    @patch('app.services.ai_service.settings')
    def test_enhance_markdown_export_disabled(self, mock_settings):
        """Test enhance_markdown_export when AI is disabled"""
        mock_settings.openai_api_key = ""
        mock_settings.ai_enabled = False
        service = AIService()
        result = service.enhance_markdown_export("Project", "Description", "Logs")
        assert result == "Description"

    @patch('app.services.ai_service.settings')
    @patch('app.services.ai_service.AIService.is_enabled', return_value=True)
    def test_enhance_markdown_export_success(self, mock_enabled, mock_settings):
        """Test successful markdown export enhancement"""
        mock_settings.openai_api_key = "test-key"
        mock_settings.ai_enabled = True

        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Enhanced summary"
            mock_client.chat.completions.create.return_value = mock_response

            service = AIService()
            result = service.enhance_markdown_export("Project", "Original", "Summary")
            assert result == "Enhanced summary"

    @patch('app.services.ai_service.settings')
    @patch('app.services.ai_service.AIService.is_enabled', return_value=True)
    def test_enhance_markdown_export_error(self, mock_enabled, mock_settings):
        """Test markdown export enhancement with error"""
        mock_settings.openai_api_key = "test-key"
        mock_settings.ai_enabled = True

        with patch('openai.OpenAI') as mock_openai:
            mock_openai.side_effect = Exception("API Error")

            service = AIService()
            result = service.enhance_markdown_export("Project", "Description", "Logs")
            assert result == "Description"

    @patch('app.services.ai_service.settings')
    @patch('app.services.ai_service.AIService.is_enabled', return_value=True)
    def test_generate_project_description_empty_tech_stack(self, mock_enabled, mock_settings):
        """Test project description generation with empty tech stack"""
        mock_settings.openai_api_key = "test-key"
        mock_settings.ai_enabled = True

        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Description without tech stack"
            mock_client.chat.completions.create.return_value = mock_response

            service = AIService()
            result = service.generate_project_description("Test Project", [])
            assert result == "Description without tech stack"

    @patch('app.services.ai_service.settings')
    @patch('app.services.ai_service.AIService.is_enabled', return_value=True)
    def test_generate_build_log_content_without_context(self, mock_enabled, mock_settings):
        """Test build log content generation without context"""
        mock_settings.openai_api_key = "test-key"
        mock_settings.ai_enabled = True

        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Content without context"
            mock_client.chat.completions.create.return_value = mock_response

            service = AIService()
            result = service.generate_build_log_content("Test Project", "update", "")
            assert result == "Content without context"
