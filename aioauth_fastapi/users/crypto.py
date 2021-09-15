import base64
import hashlib
import hmac
import math
import secrets
import string
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict

from jose import constants, jwt

from ..config import settings

RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits


def get_random_string(length, allowed_chars=RANDOM_STRING_CHARS) -> str:
    """
    Return a securely generated random string.
    The bit length of the returned value can be calculated with the formula:
        log_2(len(allowed_chars)^length)
    For example, with default `allowed_chars` (26+26+10), this gives:
      * length: 12, bit length =~ 71 bits
      * length: 22, bit length =~ 131 bits
    """
    return "".join(secrets.choice(allowed_chars) for i in range(length))


def generate_salt() -> bytes:
    """
    Generate a cryptographically secure nonce salt in ASCII with an entropy
    of at least `salt_entropy` bits.
    """
    # Each character in the salt provides
    # log_2(len(alphabet)) bits of entropy.
    char_count = math.ceil(128 / math.log2(len(RANDOM_STRING_CHARS)))
    salt = get_random_string(char_count, allowed_chars=RANDOM_STRING_CHARS)
    return salt.encode()


def pbkdf2(password: str, salt: bytes = None, iterations=100000) -> str:
    algorithm = hashlib.sha256().name

    if salt is None:
        _salt = generate_salt()
    else:
        _salt = salt

    hash = hashlib.pbkdf2_hmac(
        algorithm,  # The hash digest algorithm for HMAC
        password.encode("utf-8"),  # Convert the password to bytes
        _salt,  # Provide the salt
        iterations,  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    hash = base64.b64encode(hash).decode("ascii").strip()
    return f"{algorithm}${iterations}${_salt.decode()}${hash}"


def verify(password: str, password_db: str) -> bool:
    algorithm, iterations, salt, hash = password_db.split("$", 3)
    encoded_2 = pbkdf2(password, salt.encode(), int(iterations))
    return hmac.compare_digest(password_db.encode(), encoded_2.encode())


def make_random_password() -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(16))


def encode_jwt(
    expires_delta,
    sub,
    token_type,
    secret,
    additional_claims: Dict = {},
    algorithm=constants.ALGORITHMS.RS256,
):
    now = datetime.now(timezone.utc)

    claims = {
        "iat": now,
        "jti": str(uuid.uuid4()),
        "nbf": now,
        "type": token_type,
        "sub": sub,
        "exp": now + timedelta(seconds=expires_delta),
        **additional_claims,
    }

    return jwt.encode(
        claims,
        secret,
        algorithm,
    )


def decode_jwt(
    encoded_token,
    secret,
    algorithms=[constants.ALGORITHMS.RS256],
):
    return jwt.decode(
        encoded_token,
        secret,
        algorithms=algorithms,
    )


def get_jwt(user):
    access_token = encode_jwt(
        sub=str(user.id),
        secret=settings.JWT_PRIVATE_KEY,
        expires_delta=settings.ACCESS_TOKEN_EXP,
        token_type="access",
        additional_claims={
            "is_blocked": user.is_blocked,
            "is_superuser": user.is_superuser,
            "username": user.username,
        },
    )

    refresh_token = encode_jwt(
        sub=str(user.id),
        secret=settings.JWT_PRIVATE_KEY,
        expires_delta=settings.REFRESH_TOKEN_EXP,
        token_type="access",
        additional_claims={
            "is_blocked": user.is_blocked,
            "is_superuser": user.is_superuser,
            "username": user.username,
        },
    )

    return access_token, refresh_token
