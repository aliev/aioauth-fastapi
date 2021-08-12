INSERT INTO client (
    id,
    client_id,
    client_secret,
    grant_types,
    response_types,
    redirect_uris,
    scope
) VALUES (
    '3b23a838-b92d-409f-b49b-a1d9cb675c29',
    'be861a8a-7817-4a9e-93d3-9976bf099893',
    '71569cc8-89ea-48c1-adb3-10f831020840',
    '{"authorization_code", "password", "client_credentials", "refresh_token"}',
    '{"token", "code", "none", "id_token"}',
    '{"http://127.0.0.1:8001/api/users/callback"}',
    'read write'
);
