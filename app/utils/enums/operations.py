from enum import Enum
class Operations(Enum):
    """Operations is an enumeration of the different types of operations that can be performed on a resource.

    Args:
        CREATE (str): Indicates that a resource is being created.
        FETCH (str): Indicates that a resource is being fetched.
        UPDATE (str): Indicates that a resource is being updated.
        DELETE (str): Indicates that a resource is being deleted.
        PATCH (str): Indicates that a resource is being partially updated.
    """
    CREATE = "Creating"
    FETCH = "Fetching"
    UPDATE = "Updating"
    DELETE = "Deleting"
    PATCH = "Patching"    

