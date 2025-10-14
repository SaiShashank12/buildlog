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
        Generate build log content with rich markdown formatting

        Args:
            project_name: Name of the project
            log_type: Type of log (update, milestone, feature, bug_fix, note)
            context: Optional context or hints for generation

        Returns:
            Generated log content with markdown formatting
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
- Well-structured with markdown formatting
- Include headings (##, ###), bullet points, and **bold** text where appropriate
- If technical details are mentioned, use code blocks with backticks
- 2-3 short sections

Use markdown formatting like:
## What I Did
- Point 1
- Point 2

## Technical Details
Brief explanation with **bold** keywords.

## Next Steps
- Task 1
- Task 2

Make it engaging and informative!"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a technical writer helping document software development progress. You always use markdown formatting to make content clear and visually appealing."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating build log content: {e}")
            return ""

    def generate_project_summary(self, project_name: str, description: str, logs: list) -> str:
        """
        Generate an AI-powered summary of the entire project

        Args:
            project_name: Project name
            description: Project description
            logs: List of build logs

        Returns:
            Comprehensive project summary
        """
        if not self.enabled:
            return ""

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            # Create a summary of logs
            log_summaries = []
            for log in logs[:10]:  # Limit to last 10 logs
                log_summaries.append(f"- [{log.get('log_type')}] {log.get('title', 'Untitled')}")

            logs_text = "\n".join(log_summaries) if log_summaries else "No logs yet"

            prompt = f"""Create a comprehensive project summary with markdown formatting:

Project: {project_name}
Description: {description}

Recent Activity:
{logs_text}

Generate a professional summary that includes:
## Overview
Brief overview of the project and its purpose

## Key Achievements
- Major accomplishments
- Technical highlights

## Progress Summary
Current state and development velocity

Use markdown formatting with headings, bullet points, and **bold** text."""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing project progress and creating executive summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating project summary: {e}")
            return ""

    def suggest_tags(self, title: str, content: str) -> list:
        """
        Generate smart tag suggestions based on log content

        Args:
            title: Log title
            content: Log content

        Returns:
            List of suggested tags
        """
        if not self.enabled:
            return []

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            prompt = f"""Analyze this build log and suggest 3-5 relevant tags:

Title: {title}
Content: {content[:500]}

Suggest specific, technical tags that categorize this log entry. Return ONLY a comma-separated list of tags, nothing else.

Examples: "backend, api, database" or "frontend, ui, react, responsive"

Tags:"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a smart tagging system that extracts relevant technical keywords."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.5
            )

            tags_str = response.choices[0].message.content.strip()
            # Split by comma and clean up
            tags = [tag.strip() for tag in tags_str.split(',')]
            return tags[:5]  # Max 5 tags
        except Exception as e:
            print(f"Error suggesting tags: {e}")
            return []

    def generate_readme(self, project_name: str, description: str, tech_stack: list, logs: list) -> str:
        """
        Generate a comprehensive README from all project data

        Args:
            project_name: Project name
            description: Project description
            tech_stack: Technologies used
            logs: All build logs

        Returns:
            Complete README content in markdown
        """
        if not self.enabled:
            return ""

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            # Prepare log summaries
            log_summaries = []
            for log in logs:
                log_summaries.append(f"{log.get('created_at', '')[:10]} - {log.get('title', 'Untitled')}")

            logs_timeline = "\n".join(log_summaries[:15])  # Last 15 logs
            tech_stack_str = ", ".join(tech_stack) if tech_stack else "Various technologies"

            prompt = f"""Generate a professional README.md for this project:

Project Name: {project_name}
Description: {description}
Tech Stack: {tech_stack_str}

Development Timeline:
{logs_timeline}

Create a comprehensive README with these sections:
# Project Name

## Description
Engaging project description

## Features
- Key features (bullet points)

## Tech Stack
Technologies used with brief explanations

## Development Journey
Brief summary of the development process

## Installation
Basic setup instructions (generic)

## Usage
How to use the project

## What I Learned
Technical insights and learnings

Use proper markdown formatting with headings, lists, code blocks, and **bold** emphasis."""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert technical writer who creates professional README files for GitHub projects."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating README: {e}")
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
