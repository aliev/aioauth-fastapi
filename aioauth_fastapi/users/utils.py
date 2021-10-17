from fastapi import Request, HTTPException, status
from functools import wraps


def is_superuser(f):
    @wraps(f)
    async def wrapper(request: Request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.is_superuser
        ):
            return await f(request=request, *args, **kwargs)

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return wrapper
