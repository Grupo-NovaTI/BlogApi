from abc import ABC, abstractmethod
from typing import Optional

class FileStorageInterface(ABC):

    @abstractmethod
    async def upload_file(self, file_content: bytes, content_type: str, user_id: int, prefix: str, file_name : Optional[str] = None, replace_existing: bool = True) -> str:
        """
        Uploads a file to the storage and returns its URL.
        """
        pass

    @abstractmethod
    async def delete_file(self, file_url: str) -> None:
        """
        Deletes a file from the storage.
        """
        pass
