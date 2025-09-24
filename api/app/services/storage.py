from azure.storage.blob import BlobServiceClient
from app.core.config import get_settings

class BlobStorageService:
    def __init__(self):
        s = get_settings()
        if not s.azure_storage_conn_str:
            raise RuntimeError("AZURE_STORAGE_CONN_STR not configured")
        self.client = BlobServiceClient.from_connection_string(s.azure_storage_conn_str)
        self.container = self.client.get_container_client(s.blob_container)
        try:
            self.container.create_container()
        except Exception:
            pass

    def upload_bytes(self, name: str, content: bytes, content_type: str):
        blob = self.container.get_blob_client(name)
        blob.upload_blob(content, overwrite=True, content_type=content_type)
        return name
