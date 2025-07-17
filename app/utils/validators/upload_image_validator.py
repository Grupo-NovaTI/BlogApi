from typing import List

from fastapi import HTTPException, UploadFile
from starlette import status

from app.utils.constants.constants import (ALLOWED_MIME_TYPES,
                                           MAX_FILE_SIZE_BYTES)


async def validate_uploaded_image(file: UploadFile, image_size : int = MAX_FILE_SIZE_BYTES, allowed_types: List[str] = ALLOWED_MIME_TYPES) -> bytes:
    """
    Validates an uploaded profile picture for type and size.

    Args:
        file: The uploaded file from FastAPI.

    Returns:
        The file content as bytes if validation is successful.

    Raises:
        HTTPException: If the file type or size is invalid.
    """

    

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types are: {', '.join(allowed_types)}"
        )

    file_content: bytes = await file.read()

    if len(file_content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds the limit of {image_size / (1024*1024):.0f}MB."
        )

    return file_content
