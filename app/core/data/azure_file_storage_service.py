import uuid

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import ContentSettings
from azure.storage.blob.aio import BlobServiceClient, ContainerClient
from azure.storage.blob.aio._blob_client_async import BlobClient

from app.core.config.application_config import (
    CLOUD_STORAGE_CONNECTION_STRING, CLOUD_STORAGE_CONTAINER_NAME)
from app.utils.errors.exceptions import FileStorageException, NotFoundException
from app.core.data.file_storage_interface import FileStorageInterface


class AzureFileStorageService(FileStorageInterface):
    """
    A service for interacting with Azure Blob Storage.
    Uses the async client for compatibility with FastAPI.
    """

    def __init__(self, connection_string: str = CLOUD_STORAGE_CONNECTION_STRING, container_name: str = CLOUD_STORAGE_CONTAINER_NAME) -> None:
        self.blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(
            connection_string)
        self.container_name: str = container_name

    async def _get_container_client(self) -> ContainerClient:
        """
        Retrieves an async client for the configured container.
        Creates the container if it does not exist.
        """
        container_client: ContainerClient = self.blob_service_client.get_container_client(
            self.container_name)
        if not await container_client.exists():
            await container_client.create_container()
        return container_client

    async def upload_file(
        self,
        file_content: bytes,
        content_type: str,
        user_id: int,
        prefix: str = "profile-pictures"
    ) -> str:
        """
        Uploads a file to Azure Blob Storage and returns its URL.

        Args:
            file_content: The binary content of the file.
            content_type: The MIME type of the file.
            user_id: The ID of the user uploading the file, for organization.
            prefix: A folder-like prefix for organization within the container.

        Returns:
            The full URL of the uploaded blob.
        """
        try:
            container_client: ContainerClient = await self._get_container_client()
            file_extension: str = content_type.split(
                '/')[-1]

            blob_name: str = f"{prefix}/{user_id}/profile-picture.{file_extension}"

            async with container_client.get_blob_client(
                    blob_name) as blob_client:

                await blob_client.upload_blob(file_content, overwrite=True)

                await blob_client.set_http_headers(content_settings=ContentSettings(content_type=content_type))

                await blob_client.close()

                return blob_client.url

        except Exception as e:
            raise FileStorageException(details=str(e)) from e

    async def delete_file(self, file_url: str) -> None:
        """
        Deletes a file from Azure Blob Storage using its full URL.
        Args:
            file_url: The full URL of the blob to delete.
        Raises:
            NotFoundException: If the blob does not exist.
            FileStorageException: For other errors during deletion.

        """
        try:
            blob_name: str = file_url.split(f"/{self.container_name}/")[-1]

            container_client: ContainerClient = await self._get_container_client()
            async with container_client.get_blob_client(
                    blob_name) as blob_client:

                await blob_client.delete_blob()

        except ResourceNotFoundError:
            raise NotFoundException(
                resource_type="file", identifier=file_url)
        except Exception as e:
            raise FileStorageException(details=str(e)) from e
