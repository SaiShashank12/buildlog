"""
AI service for generating content using OpenAI
"""
from app.config import get_settings

settings = get_settings()


class AIService:
    """Service for AI-powered content generation"""

    def __init__(self):
        self.api_key = settings.openai_api_key
        self.enabled = settings.ai_enabled and bool(self.api_key)

    def is_enabled(self) -> bool:
        """Check if AI features are enabled"""
        return self.enabled

    def generate_project_description(self, project_name: str, tech_stack: list) -> str:
        """
        Generate a project description based on name and tech stack

        Args:
            project_name: Name of the project
            tech_stack: List of technologies used

        Returns:
            Generated description string
        """
        if not self.enabled:
            return ""

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            tech_stack_str = ", ".join(tech_stack) if tech_stack else "various technologies"

            prompt = f"""Generate a compelling 2-3 sentence description for a software project with the following details:

Project Name: {project_name}
Tech Stack: {tech_stack_str}

The description should be professional, concise, and highlight the project's purpose and technical approach. Make it suitable for a hackathon submission or portfolio."""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes compelling project descriptions for software projects and hackathon submissions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating project description: {e}")
            return ""

    def generate_build_log_content(self, project_name: str, log_type: str, context: str = "") -> str:
        """
        Generate build log content based on project and log type

        Args:
            project_name: Name of the project
            log_type: Type of log (update, milestone, feature, bug_fix, note)
            context: Optional context or hints for generation

        Returns:
            Generated log content
        """
        if not self.enabled:
            return ""

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            log_type_prompts = {
                "update": "a progress update describing recent work",
                "milestone": "a milestone achievement announcement",
                "feature": "a new feature implementation description",
                "bug_fix": "a bug fix explanation",
                "note": "a general development note"
            }

            log_description = log_type_prompts.get(log_type, "an update")
            context_hint = f"\nContext/Hints: {context}" if context else ""

            prompt = f"""Generate {log_description} for a software project called "{project_name}".{context_hint}

The content should be:
- Professional and technical
- 2-3 paragraphs
- Include specific technical details
- Suitable for a build log or development journal

Format it as plain text, not markdown."""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a technical writer helping document software development progress."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating build log content: {e}")
            return ""

    def enhance_markdown_export(self, project_name: str, description: str, logs_summary: str) -> str:
        """
        Generate an enhanced executive summary for markdown export

        Args:
            project_name: Project name
            description: Project description
            logs_summary: Summary of build logs

        Returns:
            Enhanced summary text
        """
        if not self.enabled:
            return description

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            prompt = f"""Create a compelling executive summary for this project's documentation:

Project: {project_name}
Description: {description}
Build Progress: {logs_summary}

Generate a professional 1-paragraph executive summary that:
- Highlights the project's value proposition
- Mentions key technical achievements
- Is suitable for judges, recruiters, or stakeholders
- Is concise but impactful"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at writing executive summaries for technical projects."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error enhancing markdown export: {e}")
            return description


# Singleton instance
ai_service = AIService()
