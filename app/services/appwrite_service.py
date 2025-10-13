from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.services.account import Account
from appwrite.services.users import Users
from appwrite.id import ID
from app.config import get_settings

settings = get_settings()


class AppwriteService:
    """Service class for Appwrite operations"""

    def __init__(self):
        # Initialize Appwrite client
        self.client = Client()
        self.client.set_endpoint(settings.appwrite_endpoint)
        self.client.set_project(settings.appwrite_project_id)
        self.client.set_key(settings.appwrite_api_key)

        # Initialize services
        self.databases = Databases(self.client)
        self.storage = Storage(self.client)
        self.account = Account(self.client)
        self.users = Users(self.client)

    # Database Operations
    async def create_project(self, user_id: str, data: dict):
        """Create a new project"""
        try:
            document = self.databases.create_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_projects_collection_id,
                document_id=ID.unique(),
                data={
                    **data,
                    "user_id": user_id,
                    "created_at": data.get("created_at"),
                    "updated_at": data.get("updated_at")
                }
            )
            return document
        except Exception as e:
            print(f"Error creating project: {e}")
            raise

    async def get_projects(self, user_id: str):
        """Get all projects for a user"""
        try:
            result = self.databases.list_documents(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_projects_collection_id,
                queries=[f'equal("user_id", "{user_id}")']
            )
            return result['documents']
        except Exception as e:
            print(f"Error getting projects: {e}")
            raise

    async def get_project(self, project_id: str):
        """Get a single project"""
        try:
            document = self.databases.get_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_projects_collection_id,
                document_id=project_id
            )
            return document
        except Exception as e:
            print(f"Error getting project: {e}")
            raise

    async def update_project(self, project_id: str, data: dict):
        """Update a project"""
        try:
            document = self.databases.update_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_projects_collection_id,
                document_id=project_id,
                data=data
            )
            return document
        except Exception as e:
            print(f"Error updating project: {e}")
            raise

    async def delete_project(self, project_id: str):
        """Delete a project"""
        try:
            self.databases.delete_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_projects_collection_id,
                document_id=project_id
            )
            return True
        except Exception as e:
            print(f"Error deleting project: {e}")
            raise

    # Build Log Operations
    async def create_build_log(self, project_id: str, data: dict):
        """Create a new build log entry"""
        try:
            document = self.databases.create_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_build_logs_collection_id,
                document_id=ID.unique(),
                data={
                    **data,
                    "project_id": project_id,
                    "created_at": data.get("created_at")
                }
            )
            return document
        except Exception as e:
            print(f"Error creating build log: {e}")
            raise

    async def get_build_logs(self, project_id: str):
        """Get all build logs for a project"""
        try:
            result = self.databases.list_documents(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_build_logs_collection_id,
                queries=[f'equal("project_id", "{project_id}")']
            )
            return result['documents']
        except Exception as e:
            print(f"Error getting build logs: {e}")
            raise

    async def update_build_log(self, log_id: str, data: dict):
        """Update a build log entry"""
        try:
            document = self.databases.update_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_build_logs_collection_id,
                document_id=log_id,
                data=data
            )
            return document
        except Exception as e:
            print(f"Error updating build log: {e}")
            raise

    async def delete_build_log(self, log_id: str):
        """Delete a build log entry"""
        try:
            self.databases.delete_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_build_logs_collection_id,
                document_id=log_id
            )
            return True
        except Exception as e:
            print(f"Error deleting build log: {e}")
            raise

    # Storage Operations
    async def upload_file(self, file_content, file_name: str):
        """Upload a file to Appwrite Storage"""
        try:
            file = self.storage.create_file(
                bucket_id=settings.appwrite_storage_bucket_id,
                file_id=ID.unique(),
                file=file_content
            )
            return file
        except Exception as e:
            print(f"Error uploading file: {e}")
            raise

    async def get_file_url(self, file_id: str):
        """Get file download URL"""
        try:
            result = self.storage.get_file_view(
                bucket_id=settings.appwrite_storage_bucket_id,
                file_id=file_id
            )
            return result
        except Exception as e:
            print(f"Error getting file URL: {e}")
            raise

    async def delete_file(self, file_id: str):
        """Delete a file from storage"""
        try:
            self.storage.delete_file(
                bucket_id=settings.appwrite_storage_bucket_id,
                file_id=file_id
            )
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            raise


# Singleton instance
appwrite_service = AppwriteService()
