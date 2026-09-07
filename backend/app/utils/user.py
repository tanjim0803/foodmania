from passlib.context import CryptContext
from jose import jwt, JWTError
from app.config import security_settings
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hash_password: str):
    return pwd_context.verify(password, hash_password)


def create_access_token(id: str):
    expires_at = datetime.now(tz=timezone.utc) + timedelta(
        minutes=security_settings.JWT_ACCESS_TOKEN_TIME_MIN
    )
    payload = {"sub": id, "exp": expires_at, "type": "access_token"}
    return jwt.encode(
        payload,
        security_settings.JWT_SECRET_KEY,
        algorithm=security_settings.JWT_ALGORITHM,
    )


def create_refresh_token(id: str):
    expires_at = datetime.now(tz=timezone.utc) + timedelta(
        days=security_settings.JWT_REFRESH_TOKEN_TIME_DAY
    )
    payload = {"sub": id, "exp": expires_at, "type": "refresh_token"}
    return jwt.encode(
        payload,
        security_settings.JWT_SECRET_KEY,
        algorithm=security_settings.JWT_ALGORITHM,
    )


def decode_token(token: str):
    return jwt.decode(
        token,
        security_settings.JWT_SECRET_KEY,
        algorithms=[security_settings.JWT_ALGORITHM],
    )
