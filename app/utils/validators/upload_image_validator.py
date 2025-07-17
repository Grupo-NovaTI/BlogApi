from typing import List

from fastapi import UploadFile

from app.utils.constants.constants import (ALLOWED_MIME_TYPES,
                                           MAX_FILE_SIZE_BYTES)
from app.utils.errors.exceptions import (InvalidFileTypeException,
                                         RequestEntityTooLargeException)


async def validate_uploaded_image(file: UploadFile, image_size: int = MAX_FILE_SIZE_BYTES, allowed_types: List[str] = ALLOWED_MIME_TYPES) -> bytes:
    """
    Validates an uploaded profile picture for type and size.

    Args:
        file: The uploaded file from FastAPI.

    Returns:
        The file content as bytes if validation is successful.

    Raises:
        HTTPException: If the file type or size is invalid.
    """

    if file.content_type is not None and file.content_type not in allowed_types:
        raise InvalidFileTypeException(
            allowed_types=allowed_types,
            provided_type=file.content_type
        )

    file_content: bytes = await file.read()

    if len(file_content) > MAX_FILE_SIZE_BYTES:
        raise RequestEntityTooLargeException(
            details=f"File size exceeds the limit of {image_size / (1024*1024):.0f}MB."
        )

    return file_content
