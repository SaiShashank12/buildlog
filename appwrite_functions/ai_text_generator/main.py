"""
AI Text Generator Function for BuildLog
Generates project descriptions and summaries using AI
"""

import os
import json


def main(context):
    """
    Main function handler for Appwrite Function

    Expected payload:
    {
        "prompt": "Write a description for my project",
        "context": "Additional context about the project",
        "max_length": 500
    }
    """

    # Parse request
    try:
        if context.req.body:
            payload = json.loads(context.req.body)
        else:
            payload = {}
    except json.JSONDecodeError:
        return context.res.json({
            "success": False,
            "error": "Invalid JSON payload"
        }, status_code=400)

    prompt = payload.get("prompt", "")
    user_context = payload.get("context", "")
    max_length = payload.get("max_length", 500)

    if not prompt:
        return context.res.json({
            "success": False,
            "error": "Prompt is required"
        }, status_code=400)

    # In a real implementation, you would call an AI API here
    # For demo purposes, we'll generate a template response

    # Example: Using OpenAI (requires OPENAI_API_KEY environment variable)
    # openai_key = os.environ.get("OPENAI_API_KEY")
    # if openai_key:
    #     import openai
    #     openai.api_key = openai_key
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant that writes compelling project descriptions."},
    #             {"role": "user", "content": f"{prompt}\n\nContext: {user_context}"}
    #         ],
    #         max_tokens=max_length
    #     )
    #     generated_text = response.choices[0].message.content

    # For now, return a template response
    generated_text = generate_template_description(prompt, user_context)

    return context.res.json({
        "success": True,
        "generated_text": generated_text,
        "prompt": prompt,
        "timestamp": context.req.headers.get("x-appwrite-timestamp", "")
    })


def generate_template_description(prompt, context):
    """
    Generate a template description based on prompt
    In production, this would call an actual AI API
    """

    templates = {
        "project_description": """
This innovative project leverages cutting-edge technologies to solve real-world problems.
Built with a focus on user experience and performance, it demonstrates best practices
in modern software development.

Key features include:
- Intuitive user interface
- Scalable architecture
- Robust error handling
- Comprehensive documentation

The project showcases technical proficiency and creative problem-solving, making it
an excellent addition to any portfolio.
        """,

        "milestone": """
Reached a significant milestone in the project development! This achievement represents
hours of dedication, problem-solving, and iterative improvements. The implementation
demonstrates solid understanding of core concepts and practical application of best practices.
        """,

        "feature": """
Implemented a new feature that enhances functionality and improves user experience.
This addition showcases technical skills and attention to detail, contributing to
the overall value and usability of the project.
        """,

        "summary": """
Comprehensive project that demonstrates full-stack development capabilities.
From concept to deployment, every aspect has been carefully crafted to deliver
a polished, production-ready application.
        """
    }

    # Simple keyword matching for demo
    prompt_lower = prompt.lower()

    if "description" in prompt_lower or "describe" in prompt_lower:
        return templates["project_description"].strip()
    elif "milestone" in prompt_lower:
        return templates["milestone"].strip()
    elif "feature" in prompt_lower:
        return templates["feature"].strip()
    elif "summary" in prompt_lower or "summarize" in prompt_lower:
        return templates["summary"].strip()
    else:
        return templates["project_description"].strip()


# Appwrite Function entry point
if __name__ == "__main__":
    # This is called when testing locally
    class MockContext:
        class MockReq:
            body = '{"prompt": "Write a description for my project", "context": "A web app built with Python and FastAPI"}'
            headers = {"x-appwrite-timestamp": "2025-10-13"}

        class MockRes:
            @staticmethod
            def json(data, status_code=200):
                return {"data": data, "status": status_code}

        req = MockReq()
        res = MockRes()

    result = main(MockContext())
    print(json.dumps(result, indent=2))
