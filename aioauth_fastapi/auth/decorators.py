import functools
from http import HTTPStatus

from fastapi.exceptions import HTTPException
from starlette.requests import Request


def auth_required():
    def decorator(f):
        @functools.wraps(f)
        async def wrapper(*args, request: Request, **kwargs):
            if request.user.is_authenticated and not request.user.is_blocked:
                return await f(*args, request=request, **kwargs)

            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Permission denied."
            )

        return wrapper

    return decorator
