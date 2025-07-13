"""
Schema for password update requests with validation.
This module defines a Pydantic model for password update requests, including validation.
"""

from dataclasses import field
import re
from turtle import mode

from pydantic import BaseModel, Field, field_validator, model_validator

from app.utils.constants.constants import PASSWORD_PATTERN

class UpdatePasswordRequest(BaseModel):
    """
    Schema for password update requests.

    Validates the new password to ensure it meets security requirements.
    """
    current_password: str = Field(..., min_length=8, max_length=12, examples=["Password123!"])
    new_password: str = Field(..., min_length=8, max_length=12, examples=["Password456!"])

    @field_validator("new_password")
    def validate_new_password(cls, value: str) -> str:
        """
        Validates the new password to ensure it meets security requirements using a single regex.
        - At least one uppercase letter.
        - At least one digit.
        - At least one special character (!@#$%^&*+.).
        - At least 8 characters long.
        """
        if not re.fullmatch(pattern=PASSWORD_PATTERN, string=value):
            raise ValueError(
                "New password must be at least 8 characters long and include at least one uppercase letter, "
                "one lowercase letter, one number, and one special character (!@#$%^&*+.)."
            )
        return value
    
    @model_validator(mode="after")
    def check_passwords_not_equal(self) -> "UpdatePasswordRequest":
        """
        Ensures that the current password and new password are not the same.
        """
        if self.current_password == self.new_password:
            raise ValueError("Current password and new password cannot be the same.")
        return self