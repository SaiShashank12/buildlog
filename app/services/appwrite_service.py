import requests
from appwrite.id import ID
from app.config import get_settings

settings = get_settings()


class AppwriteService:
    """Service class for Appwrite operations using direct HTTP requests"""

    def __init__(self):
        self.endpoint = settings.appwrite_endpoint
        self.project_id = settings.appwrite_project_id
        self.api_key = settings.appwrite_api_key
        self.database_id = settings.appwrite_database_id
        self.projects_collection_id = settings.appwrite_projects_collection_id
        self.build_logs_collection_id = settings.appwrite_build_logs_collection_id
        self.storage_bucket_id = settings.appwrite_storage_bucket_id

    def _get_headers(self):
        """Get common headers for API requests"""
        return {
            "X-Appwrite-Project": self.project_id,
            "X-Appwrite-Key": self.api_key,
            "Content-Type": "application/json"
        }

    # Database Operations
    def create_project(self, user_id: str, data: dict):
        """Create a new project"""
        try:
            url = f"{self.endpoint}/databases/{self.database_id}/collections/{self.projects_collection_id}/documents"

            # Filter out None and empty string values
            clean_data = {k: v for k, v in data.items() if v is not None and v != ""}
            clean_data["user_id"] = user_id

            payload = {
                "documentId": ID.unique(),
                "data": clean_data
            }

            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error creating project: {e}")
            raise

    def get_projects(self, user_id: str):
        """Get all projects for a user"""
        try:
            url = f"{self.endpoint}/databases/{self.database_id}/collections/{self.projects_collection_id}/documents"
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()['documents']
        except Exception as e:
            print(f"Error getting projects: {e}")
            raise

    def get_project(self, project_id: str):
        """Get a single project"""
        try:
            url = f"{self.endpoint}/databases/{self.database_id}/collections/{self.projects_collection_id}/documents/{project_id}"
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting project: {e}")
            raise

    def update_project(self, project_id: str, data: dict):
        """Update a project"""
        try:
            url = f"{self.endpoint}/databases/{self.database_id}/collections/{self.projects_collection_id}/documents/{project_id}"
            # Filter out None and empty string values
            clean_data = {k: v for k, v in data.items() if v is not None and v != ""}
            payload = {"data": clean_data}
            response = requests.patch(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error updating project: {e}")
            raise

    def delete_project(self, project_id: str):
        """Delete a project"""
        try:
            url = f"{self.endpoint}/databases/{self.database_id}/collections/{self.projects_collection_id}/documents/{project_id}"
            response = requests.delete(url, headers=self._get_headers())
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error deleting project: {e}")
            raise

    # Build Log Operations
    def create_build_log(self, project_id: str, data: dict):
        """Create a new build log entry"""
        try:
            url = f"{self.endpoint}/databases/{self.database_id}/collections/{self.build_logs_collection_id}/documents"

            # Filter out None and empty values
            clean_data = {k: v for k, v in data.items() if v is not None and v != "" and v != []}
            clean_data["project_id"] = project_id
            if "created_at" in data:
                clean_data["created_at"] = data["created_at"]

            payload = {
                "documentId": ID.unique(),
                "data": clean_data
            }

            print(f"Creating build log with payload: {payload}")
            response = requests.post(url, headers=self._get_headers(), json=payload)
            print(f"Response status: {response.status_code}")
            if response.status_code != 201:
                print(f"Response body: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error creating build log: {e}")
            raise

    def get_build_logs(self, project_id: str):
        """Get all build logs for a project"""
        try:
            url = f"{self.endpoint}/databases/{self.database_id}/collections/{self.build_logs_collection_id}/documents"
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            # Filter by project_id client-side for now
            all_logs = response.json()['documents']
            return [log for log in all_logs if log.get('project_id') == project_id]
        except Exception as e:
            print(f"Error getting build logs: {e}")
            raise

    def update_build_log(self, log_id: str, data: dict):
        """Update a build log entry"""
        try:
            url = f"{self.endpoint}/databases/{self.database_id}/collections/{self.build_logs_collection_id}/documents/{log_id}"
            payload = {"data": data}
            response = requests.patch(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error updating build log: {e}")
            raise

    def delete_build_log(self, log_id: str):
        """Delete a build log entry"""
        try:
            url = f"{self.endpoint}/databases/{self.database_id}/collections/{self.build_logs_collection_id}/documents/{log_id}"
            response = requests.delete(url, headers=self._get_headers())
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error deleting build log: {e}")
            raise

    # Storage Operations (keeping SDK for file uploads as they work differently)
    def upload_file(self, file_content, file_name: str):
        """Upload a file to Appwrite Storage"""
        try:
            # For file uploads, we'll use multipart/form-data directly
            url = f"{self.endpoint}/storage/buckets/{self.storage_bucket_id}/files"

            files = {
                'fileId': (None, ID.unique()),
                'file': (file_name, file_content)
            }

            headers = {
                "X-Appwrite-Project": self.project_id,
                "X-Appwrite-Key": self.api_key
            }

            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error uploading file: {e}")
            raise

    def get_file_url(self, file_id: str):
        """Get file download URL"""
        return f"{self.endpoint}/storage/buckets/{self.storage_bucket_id}/files/{file_id}/view"

    def delete_file(self, file_id: str):
        """Delete a file from storage"""
        try:
            url = f"{self.endpoint}/storage/buckets/{self.storage_bucket_id}/files/{file_id}"
            response = requests.delete(url, headers=self._get_headers())
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            raise


# Singleton instance
appwrite_service = AppwriteService()
