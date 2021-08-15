Install requirements:

```
pip install -e ."[dev]"
```

Apply migrations

```
alembic upgrade head
```

Create client for demo

```sql
INSERT INTO client (
    id,
    client_id,
    client_secret,
    grant_types,
    response_types,
    redirect_uris,
    scope
) VALUES (
    '3b23a838-b92d-409f-b49b-a1d9cb675c29', -- id
    'be861a8a-7817-4a9e-93d3-9976bf099893', -- client_id
    '71569cc8-89ea-48c1-adb3-10f831020840', -- client_secret
    '{"authorization_code", "password", "client_credentials", "refresh_token"}', -- grant_types
    '{"token", "code", "none", "id_token"}', -- response_types
    '{"https://oidcdebugger.com/debug", "https://openidconnect.net/callback"}', -- redirect_uris
    'read write' -- scope
);
```

Create .env file:

```
PSQL_DSN=postgresql+asyncpg://user@localhost/database
DEBUG=True
JWT_PRIVATE_KEY=''
JWT_PUBLIC_KEY=''
```

Run server

```
python -m aioauth_fastapi
```
