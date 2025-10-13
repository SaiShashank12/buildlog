from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProjectCreate(BaseModel):
    """Schema for creating a new project"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = []
    repository_url: Optional[str] = None
    demo_url: Optional[str] = None
    tags: Optional[List[str]] = []


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    repository_url: Optional[str] = None
    demo_url: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None  # planning, in_progress, completed, on_hold


class BuildLogCreate(BaseModel):
    """Schema for creating a build log entry"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    log_type: str = "update"  # update, milestone, bug_fix, feature, note
    code_snippets: Optional[List[dict]] = []
    images: Optional[List[str]] = []  # File IDs from Appwrite Storage
    links: Optional[List[dict]] = []
    tags: Optional[List[str]] = []


class BuildLogUpdate(BaseModel):
    """Schema for updating a build log entry"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    log_type: Optional[str] = None
    code_snippets: Optional[List[dict]] = None
    images: Optional[List[str]] = None
    links: Optional[List[dict]] = None
    tags: Optional[List[str]] = None


class UserLogin(BaseModel):
    """Schema for user login"""
    email: str
    password: str


class UserRegister(BaseModel):
    """Schema for user registration"""
    email: str
    password: str
    name: str


class MarkdownExportRequest(BaseModel):
    """Schema for markdown export request"""
    project_id: str
    include_logs: bool = True
    include_images: bool = True
    include_code_snippets: bool = True


class AIGenerateRequest(BaseModel):
    """Schema for AI text generation request"""
    prompt: str = Field(..., min_length=1)
    context: Optional[str] = None
    max_length: Optional[int] = 500
