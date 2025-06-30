from typing import List, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address



def get_rate_limiter(storage_uri : Optional[str] = None, default_limits : List = ["5/minute"]) -> Limiter:
    """
    Create and return a rate limiter instance.
    
    This function initializes a SlowAPI Limiter with a default key function
    that uses the remote address of the request.
    
    Parameters:
        storage_uri (Optional[str]): The URI for the storage backend. If None, defaults to in-memory storage.
        default_limits (List): A list of default rate limits to apply. Defaults to ["5/minute"].
    
    Returns:
        Limiter: An instance of SlowAPI Limiter.
    """
    return Limiter(key_func=get_remote_address, default_limits=default_limits, storage_uri=storage_uri)