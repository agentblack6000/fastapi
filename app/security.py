from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.exceptions import InvalidKey
import os

from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ITERATIONS = 3
MEMORY_COST = 65536
LANES = 4
HASH_LENGTH = 32
SALT_SIZE = 16


def hash_password(password: str) -> bytes:
    """
    Hashes a plain-text password using Argon2id.
    Returns a combined byte string containing [salt] + [hashed_password].
    """
    salt = os.urandom(SALT_SIZE)

    argon2 = Argon2id(
        length=HASH_LENGTH,
        iterations=ITERATIONS,
        lanes=LANES,
        memory_cost=MEMORY_COST,
        salt=salt,
    )

    hashed = argon2.derive(password.encode("utf-8"))

    return salt + hashed


def verify_password(password: str, stored_hash: bytes) -> bool:
    """
    Verifies a plain-text password against the stored byte string.
    """
    # Extract the salt and hashed password
    salt = stored_hash[:SALT_SIZE]
    raw_hash = stored_hash[SALT_SIZE:]

    # Re-configure Argon2id with the exact same salt extracted from the database
    argon2 = Argon2id(
        memory_cost=MEMORY_COST,
        iterations=ITERATIONS,
        lanes=LANES,
        salt=salt,
        length=HASH_LENGTH,
    )

    try:
        # Compare securely
        argon2.verify(password.encode("utf-8"), raw_hash)
        return True
    except InvalidKey:
        # The password didn't match
        return False


def create_access_token(data: dict):
    """Generates a secure JWT token containing the user's data."""
    token_data = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data.update({"exp": expire})

    encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    """Decodes JWT tokens. Returns the decoded payload if valid, otherwise None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return None
