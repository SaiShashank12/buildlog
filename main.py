from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import markdown
from typing import Optional, List
import json

from app.config import get_settings
from app.services.appwrite_service import appwrite_service
from app.services.ai_service import ai_service
from app.services.analytics_service import AnalyticsService
from app.models.schemas import (
    ProjectCreate, ProjectUpdate, BuildLogCreate, BuildLogUpdate
)

# Initialize FastAPI app
app = FastAPI(
    title="BuildLog",
    description="AI-Powered Hackathon & Project Documentation Platform",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

settings = get_settings()

# Initialize analytics service
analytics_service = AnalyticsService(appwrite_service)


# Authentication dependency
async def get_current_user(request: Request):
    """Get current user from session cookie"""
    session_token = request.cookies.get("session")

    if not session_token:
        raise HTTPException(
            status_code=302,
            detail="Not authenticated",
            headers={"Location": "/login"}
        )

    try:
        user = appwrite_service.get_account(session_token)
        return user
    except Exception as e:
        print(f"Error getting user from session: {e}")
        raise HTTPException(
            status_code=302,
            detail="Invalid session",
            headers={"Location": "/login"}
        )


async def get_current_user_optional(request: Request):
    """Get current user from session cookie, returns None if not authenticated"""
    session_token = request.cookies.get("session")

    if not session_token:
        return None

    try:
        user = appwrite_service.get_account(session_token)
        return user
    except Exception:
        return None


# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Homepage - redirect to dashboard if logged in, otherwise show landing page"""
    user = await get_current_user_optional(request)

    if user:
        return RedirectResponse(url="/dashboard", status_code=302)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "BuildLog - Document Your Journey",
        "user": None
    })


# Authentication Routes
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Show login page"""
    user = await get_current_user_optional(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)

    return templates.TemplateResponse("login.html", {
        "request": request,
        "title": "Login",
        "user": None,
        "error": None
    })


@app.post("/login")
async def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...)
):
    """Handle login form submission"""
    try:
        # Create session with Appwrite
        session = appwrite_service.create_session(email, password)

        # Create redirect response
        redirect = RedirectResponse(url="/dashboard", status_code=303)

        # Store session token in cookie
        redirect.set_cookie(
            key="session",
            value=session["secret"],
            httponly=True,
            max_age=60 * 60 * 24 * 30,  # 30 days
            samesite="lax"
        )

        # Store session ID in cookie for logout
        redirect.set_cookie(
            key="session_id",
            value=session["$id"],
            httponly=True,
            max_age=60 * 60 * 24 * 30,  # 30 days
            samesite="lax"
        )

        return redirect

    except Exception as e:
        print(f"Login error: {e}")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "title": "Login",
            "user": None,
            "error": "Invalid email or password. Please try again."
        }, status_code=401)


@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Show signup page"""
    user = await get_current_user_optional(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)

    return templates.TemplateResponse("signup.html", {
        "request": request,
        "title": "Sign Up",
        "user": None,
        "error": None
    })


@app.post("/signup")
async def signup(
    request: Request,
    response: Response,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """Handle signup form submission"""
    try:
        # Create account with Appwrite
        appwrite_service.create_account(email, password, name)

        # Automatically log in after signup
        session = appwrite_service.create_session(email, password)

        # Create redirect response
        redirect = RedirectResponse(url="/dashboard", status_code=303)

        # Store session token in cookie
        redirect.set_cookie(
            key="session",
            value=session["secret"],
            httponly=True,
            max_age=60 * 60 * 24 * 30,  # 30 days
            samesite="lax"
        )

        # Store session ID in cookie for logout
        redirect.set_cookie(
            key="session_id",
            value=session["$id"],
            httponly=True,
            max_age=60 * 60 * 24 * 30,  # 30 days
            samesite="lax"
        )

        return redirect

    except Exception as e:
        error_message = str(e)
        if "user already exists" in error_message.lower() or "already exists" in error_message.lower():
            error_message = "An account with this email already exists. Please login instead."
        else:
            error_message = "Unable to create account. Please try again."

        print(f"Signup error: {e}")
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "title": "Sign Up",
            "user": None,
            "error": error_message
        }, status_code=400)


@app.get("/logout")
async def logout(request: Request):
    """Handle logout"""
    try:
        session_token = request.cookies.get("session")
        session_id = request.cookies.get("session_id")

        if session_token and session_id:
            try:
                appwrite_service.delete_session(session_token, session_id)
            except Exception as e:
                print(f"Error deleting session: {e}")

        # Create redirect response
        redirect = RedirectResponse(url="/", status_code=303)

        # Clear session cookies
        redirect.delete_cookie("session")
        redirect.delete_cookie("session_id")

        return redirect

    except Exception as e:
        print(f"Logout error: {e}")
        redirect = RedirectResponse(url="/", status_code=303)
        redirect.delete_cookie("session")
        redirect.delete_cookie("session_id")
        return redirect


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: dict = Depends(get_current_user)):
    """User dashboard with all projects"""
    try:
        projects = appwrite_service.get_projects(user["$id"])

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "title": "Dashboard",
            "projects": projects,
            "user": user
        })
    except Exception as e:
        print(f"Error loading dashboard: {e}")
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "title": "Dashboard",
            "projects": [],
            "user": user
        })


@app.get("/analytics", response_class=HTMLResponse)
async def analytics_dashboard(request: Request, user: dict = Depends(get_current_user)):
    """Analytics dashboard with charts and statistics"""
    try:
        return templates.TemplateResponse("analytics.html", {
            "request": request,
            "title": "Analytics",
            "user": user
        })
    except Exception as e:
        print(f"Error loading analytics: {e}")
        raise HTTPException(status_code=500, detail="Error loading analytics dashboard")


@app.get("/api/analytics")
async def get_analytics(request: Request, user: dict = Depends(get_current_user)):
    """Get analytics data"""
    try:
        analytics = analytics_service.get_complete_analytics(user["$id"])
        return JSONResponse(analytics)
    except Exception as e:
        print(f"Error getting analytics: {e}")
        return JSONResponse({
            "error": str(e)
        }, status_code=500)


@app.get("/projects/new", response_class=HTMLResponse)
async def new_project_form(request: Request, user: dict = Depends(get_current_user)):
    """Show create project form"""
    return templates.TemplateResponse("project_form.html", {
        "request": request,
        "title": "Create New Project",
        "user": user,
        "project": None
    })


@app.post("/projects/new")
async def create_project(
    request: Request,
    user: dict = Depends(get_current_user),
    name: str = Form(...),
    description: str = Form(""),
    tech_stack: str = Form(""),
    repository_url: str = Form(""),
    demo_url: str = Form(""),
    tags: str = Form("")
):
    """Create a new project"""
    try:

        project_data = {
            "name": name,
            "description": description,
            "tech_stack": tech_stack.split(",") if tech_stack else [],
            "repository_url": repository_url if repository_url else None,
            "demo_url": demo_url if demo_url else None,
            "tags": tags.split(",") if tags else [],
            "status": "in_progress",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        project = appwrite_service.create_project(user["$id"], project_data)
        return RedirectResponse(url=f"/projects/{project['$id']}", status_code=303)
    except Exception as e:
        print(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/projects/{project_id}", response_class=HTMLResponse)
async def view_project(request: Request, project_id: str, user: dict = Depends(get_current_user)):
    """View single project with all build logs"""
    try:
        project = appwrite_service.get_project(project_id)
        build_logs = appwrite_service.get_build_logs(project_id)

        # Sort build logs by created_at (newest first)
        build_logs.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        return templates.TemplateResponse("project_detail.html", {
            "request": request,
            "title": project.get("name", "Project"),
            "project": project,
            "build_logs": build_logs,
            "user": user
        })
    except Exception as e:
        print(f"Error loading project: {e}")
        raise HTTPException(status_code=404, detail="Project not found")


@app.get("/projects/{project_id}/edit", response_class=HTMLResponse)
async def edit_project_form(request: Request, project_id: str, user: dict = Depends(get_current_user)):
    """Show edit project form"""
    try:
        project = appwrite_service.get_project(project_id)

        return templates.TemplateResponse("project_form.html", {
            "request": request,
            "title": f"Edit {project.get('name')}",
            "user": user,
            "project": project
        })
    except Exception as e:
        print(f"Error loading project for edit: {e}")
        raise HTTPException(status_code=404, detail="Project not found")


@app.post("/projects/{project_id}/edit")
async def update_project(
    request: Request,
    project_id: str,
    user: dict = Depends(get_current_user),
    name: str = Form(...),
    description: str = Form(""),
    tech_stack: str = Form(""),
    repository_url: str = Form(""),
    demo_url: str = Form(""),
    tags: str = Form(""),
    status: str = Form("in_progress")
):
    """Update a project"""
    try:
        project_data = {
            "name": name,
            "description": description,
            "tech_stack": tech_stack.split(",") if tech_stack else [],
            "repository_url": repository_url if repository_url else None,
            "demo_url": demo_url if demo_url else None,
            "tags": tags.split(",") if tags else [],
            "status": status,
            "updated_at": datetime.now().isoformat()
        }

        appwrite_service.update_project(project_id, project_data)
        return RedirectResponse(url=f"/projects/{project_id}", status_code=303)
    except Exception as e:
        print(f"Error updating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/projects/{project_id}/delete")
async def delete_project(request: Request, project_id: str, user: dict = Depends(get_current_user)):
    """Delete a project"""
    try:
        appwrite_service.delete_project(project_id)
        return RedirectResponse(url="/dashboard", status_code=303)
    except Exception as e:
        print(f"Error deleting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/projects/{project_id}/status/{new_status}")
async def update_project_status(
    request: Request,
    project_id: str,
    new_status: str,
    user: dict = Depends(get_current_user)
):
    """Quick update project status"""
    try:
        # Validate status
        valid_statuses = ["planning", "in_progress", "completed", "on_hold"]
        if new_status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status")

        # Update only the status field
        project_data = {
            "status": new_status,
            "updated_at": datetime.now().isoformat()
        }

        appwrite_service.update_project(project_id, project_data)
        return RedirectResponse(url=f"/projects/{project_id}", status_code=303)
    except Exception as e:
        print(f"Error updating project status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/projects/{project_id}/logs/new", response_class=HTMLResponse)
async def new_log_form(request: Request, project_id: str, user: dict = Depends(get_current_user)):
    """Show create build log form"""
    try:
        project = appwrite_service.get_project(project_id)

        return templates.TemplateResponse("log_form.html", {
            "request": request,
            "title": f"New Log for {project.get('name')}",
            "user": user,
            "project": project,
            "log": None
        })
    except Exception as e:
        print(f"Error loading log form: {e}")
        raise HTTPException(status_code=404, detail="Project not found")


@app.post("/projects/{project_id}/logs/new")
async def create_build_log(
    request: Request,
    project_id: str,
    user: dict = Depends(get_current_user),
    title: str = Form(...),
    content: str = Form(...),
    log_type: str = Form("update"),
    tags: str = Form("")
):
    """Create a new build log entry"""
    try:
        log_data = {
            "title": title,
            "content": content,
            "log_type": log_type,
            "tags": tags.split(",") if tags else [],
            "code_snippets": [],
            "images": [],
            "links": [],
            "created_at": datetime.now().isoformat()
        }

        appwrite_service.create_build_log(project_id, log_data)
        return RedirectResponse(url=f"/projects/{project_id}", status_code=303)
    except Exception as e:
        print(f"Error creating build log: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/projects/{project_id}/logs/{log_id}/edit", response_class=HTMLResponse)
async def edit_log_form(request: Request, project_id: str, log_id: str, user: dict = Depends(get_current_user)):
    """Show edit build log form"""
    try:
        project = appwrite_service.get_project(project_id)

        # Get the specific log
        build_logs = appwrite_service.get_build_logs(project_id)
        log = next((log for log in build_logs if log["$id"] == log_id), None)

        if not log:
            raise HTTPException(status_code=404, detail="Log not found")

        return templates.TemplateResponse("log_form.html", {
            "request": request,
            "title": f"Edit Log",
            "user": user,
            "project": project,
            "log": log
        })
    except Exception as e:
        print(f"Error loading log for edit: {e}")
        raise HTTPException(status_code=404, detail="Log not found")


@app.post("/projects/{project_id}/logs/{log_id}/edit")
async def update_build_log(
    request: Request,
    project_id: str,
    log_id: str,
    user: dict = Depends(get_current_user),
    title: str = Form(...),
    content: str = Form(...),
    log_type: str = Form("update"),
    tags: str = Form("")
):
    """Update a build log entry"""
    try:
        log_data = {
            "title": title,
            "content": content,
            "log_type": log_type,
            "tags": tags.split(",") if tags else []
        }

        appwrite_service.update_build_log(log_id, log_data)
        return RedirectResponse(url=f"/projects/{project_id}", status_code=303)
    except Exception as e:
        print(f"Error updating build log: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/projects/{project_id}/logs/{log_id}/delete")
async def delete_build_log(request: Request, project_id: str, log_id: str, user: dict = Depends(get_current_user)):
    """Delete a build log entry"""
    try:
        appwrite_service.delete_build_log(log_id)
        return RedirectResponse(url=f"/projects/{project_id}", status_code=303)
    except Exception as e:
        print(f"Error deleting build log: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/projects/{project_id}/export", response_class=HTMLResponse)
async def export_to_markdown(request: Request, project_id: str, user: dict = Depends(get_current_user)):
    """Export project to markdown"""
    try:
        project = appwrite_service.get_project(project_id)
        build_logs = appwrite_service.get_build_logs(project_id)

        # Sort build logs by created_at
        build_logs.sort(key=lambda x: x.get("created_at", ""))

        # Generate markdown
        md_content = f"# {project.get('name')}\n\n"
        md_content += f"{project.get('description', '')}\n\n"

        if project.get('tech_stack'):
            md_content += f"**Tech Stack:** {', '.join(project.get('tech_stack', []))}\n\n"

        if project.get('repository_url'):
            md_content += f"**Repository:** {project.get('repository_url')}\n\n"

        if project.get('demo_url'):
            md_content += f"**Demo:** {project.get('demo_url')}\n\n"

        md_content += "## Build Log\n\n"

        for log in build_logs:
            md_content += f"### {log.get('title')} ({log.get('log_type')})\n\n"
            md_content += f"*{log.get('created_at', '')}*\n\n"
            md_content += f"{log.get('content', '')}\n\n"

        md_content += "\n---\n\n"
        md_content += "Generated with [BuildLog](https://github.com/yourusername/buildlog) - AI-Powered Project Documentation Platform\n"

        return templates.TemplateResponse("export.html", {
            "request": request,
            "title": f"Export {project.get('name')}",
            "project": project,
            "markdown_content": md_content
        })
    except Exception as e:
        print(f"Error exporting to markdown: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/portfolio/{project_id}", response_class=HTMLResponse)
async def public_portfolio(request: Request, project_id: str):
    """Public portfolio page for a project"""
    try:
        project = appwrite_service.get_project(project_id)
        build_logs = appwrite_service.get_build_logs(project_id)

        # Sort build logs by created_at
        build_logs.sort(key=lambda x: x.get("created_at", ""))

        return templates.TemplateResponse("portfolio.html", {
            "request": request,
            "title": project.get('name'),
            "project": project,
            "build_logs": build_logs
        })
    except Exception as e:
        print(f"Error loading portfolio: {e}")
        raise HTTPException(status_code=404, detail="Project not found")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to Appwrite Storage"""
    try:
        file_content = await file.read()
        uploaded_file = appwrite_service.upload_file(file_content, file.filename)

        return JSONResponse({
            "success": True,
            "file_id": uploaded_file["$id"],
            "filename": file.filename
        })
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# AI-powered endpoints
@app.post("/ai/generate-description")
async def generate_project_description(
    project_name: str = Form(...),
    tech_stack: str = Form("")
):
    """Generate AI-powered project description"""
    try:
        if not ai_service.is_enabled():
            return JSONResponse({
                "success": False,
                "error": "AI features are not enabled. Please configure OPENAI_API_KEY in your environment."
            }, status_code=400)

        tech_stack_list = [t.strip() for t in tech_stack.split(",")] if tech_stack else []
        description = ai_service.generate_project_description(project_name, tech_stack_list)

        if not description:
            return JSONResponse({
                "success": False,
                "error": "Failed to generate description"
            }, status_code=500)

        return JSONResponse({
            "success": True,
            "description": description
        })
    except Exception as e:
        print(f"Error generating description: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)


@app.post("/ai/generate-log-content")
async def generate_build_log_content(
    project_name: str = Form(...),
    log_type: str = Form("update"),
    context: str = Form("")
):
    """Generate AI-powered build log content"""
    try:
        if not ai_service.is_enabled():
            return JSONResponse({
                "success": False,
                "error": "AI features are not enabled. Please configure OPENAI_API_KEY in your environment."
            }, status_code=400)

        content = ai_service.generate_build_log_content(project_name, log_type, context)

        if not content:
            return JSONResponse({
                "success": False,
                "error": "Failed to generate content"
            }, status_code=500)

        return JSONResponse({
            "success": True,
            "content": content
        })
    except Exception as e:
        print(f"Error generating log content: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)


@app.get("/ai/status")
async def ai_status():
    """Check if AI features are enabled"""
    return JSONResponse({
        "enabled": ai_service.is_enabled()
    })


@app.post("/ai/generate-summary")
async def generate_project_summary(
    project_id: str = Form(...)
):
    """Generate AI-powered project summary"""
    try:
        if not ai_service.is_enabled():
            return JSONResponse({
                "success": False,
                "error": "AI features are not enabled. Please configure OPENAI_API_KEY in your environment."
            }, status_code=400)

        # Get project and logs
        project = appwrite_service.get_project(project_id)
        build_logs = appwrite_service.get_build_logs(project_id)

        # Sort logs by created_at (newest first)
        build_logs.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        summary = ai_service.generate_project_summary(
            project.get("name", ""),
            project.get("description", ""),
            build_logs
        )

        if not summary:
            return JSONResponse({
                "success": False,
                "error": "Failed to generate summary"
            }, status_code=500)

        return JSONResponse({
            "success": True,
            "summary": summary
        })
    except Exception as e:
        print(f"Error generating project summary: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)


@app.post("/ai/suggest-tags")
async def suggest_tags(
    title: str = Form(...),
    content: str = Form("")
):
    """Generate AI-powered tag suggestions"""
    try:
        if not ai_service.is_enabled():
            return JSONResponse({
                "success": False,
                "error": "AI features are not enabled. Please configure OPENAI_API_KEY in your environment."
            }, status_code=400)

        tags = ai_service.suggest_tags(title, content)

        if not tags:
            return JSONResponse({
                "success": False,
                "error": "Failed to generate tags"
            }, status_code=500)

        return JSONResponse({
            "success": True,
            "tags": tags
        })
    except Exception as e:
        print(f"Error suggesting tags: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)


@app.post("/ai/generate-readme")
async def generate_readme(
    project_id: str = Form(...)
):
    """Generate AI-powered README from project data"""
    try:
        if not ai_service.is_enabled():
            return JSONResponse({
                "success": False,
                "error": "AI features are not enabled. Please configure OPENAI_API_KEY in your environment."
            }, status_code=400)

        # Get project and logs
        project = appwrite_service.get_project(project_id)
        build_logs = appwrite_service.get_build_logs(project_id)

        # Sort logs by created_at
        build_logs.sort(key=lambda x: x.get("created_at", ""))

        readme = ai_service.generate_readme(
            project.get("name", ""),
            project.get("description", ""),
            project.get("tech_stack", []),
            build_logs
        )

        if not readme:
            return JSONResponse({
                "success": False,
                "error": "Failed to generate README"
            }, status_code=500)

        return JSONResponse({
            "success": True,
            "readme": readme
        })
    except Exception as e:
        print(f"Error generating README: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "BuildLog API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
