"""
Defines the Operations enumeration for resource actions in the application.

This module provides a standardized set of operation names to be used for logging, exception handling,
and service/repository logic throughout the codebase. Each operation represents a common CRUD or resource
manipulation action.
"""

from enum import Enum


class Operations(Enum):
    """
    Enumeration of the different types of operations that can be performed on a resource.

    Attributes:
        CREATE (str): Indicates that a resource is being created.
        FETCH (str): Indicates that a resource is being fetched.
        FETCH_ALL (str): Indicates that all resources are being fetched.
        FETCH_BY (str): Indicates that a resource is being fetched by a specific identifier.
        UPDATE (str): Indicates that a resource is being updated.
        DELETE (str): Indicates that a resource is being deleted.
        PATCH (str): Indicates that a resource is being partially updated.
        AUTHENTICATE (str): Indicates that a user is being authenticated.
    """

    CREATE = "Creating"
    FETCH = "Fetching"
    FETCH_ALL = "Fetching All"
    FETCH_BY = "Fetching By Specific Identifier"
    UPDATE = "Updating"
    DELETE = "Deleting"
    PATCH = "Patching"
    AUTHENTICATE = "Authenticating"

