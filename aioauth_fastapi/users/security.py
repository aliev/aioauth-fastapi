from fastapi import Security
from fastapi.security import APIKeyHeader


api_key = APIKeyHeader(name="authorization", auto_error=False)
api_security = Security(api_key)
