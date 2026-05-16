"""
Authentication and JWT token management for Executive Agent Platform

Implements JWT-based authentication with user context, roles, and permissions.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import ExpiredSignatureError, JWTError, jwt
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import structlog
from pydantic import BaseModel

logger = structlog.get_logger()

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production-with-32-char-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))

security = HTTPBearer(auto_error=False)


class TokenData(BaseModel):
    """JWT token claims"""
    user_id: str
    user_email: Optional[str] = None
    roles: list[str] = []
    permissions: list[str] = []
    iss: str = "executive-agent"
    aud: str = "api"
    iat: Optional[int] = None
    exp: Optional[int] = None


class UserContext(BaseModel):
    """Authenticated user context"""
    user_id: str
    email: Optional[str] = None
    roles: list[str] = []
    permissions: list[str] = []
    is_authenticated: bool = True
    issued_at: datetime
    expires_at: datetime


def create_access_token(
    user_id: str,
    email: Optional[str] = None,
    roles: Optional[list[str]] = None,
    permissions: Optional[list[str]] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token

    Args:
        user_id: Unique user identifier
        email: User email address
        roles: List of user roles (admin, operator, viewer)
        permissions: List of specific permissions
        expires_delta: Custom expiration time

    Returns:
        JWT token string

    Raises:
        HTTPException: If token creation fails
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    now = datetime.now(timezone.utc)

    token_data = {
        "sub": user_id,  # subject
        "email": email,
        "roles": roles or ["user"],
        "permissions": permissions or [],
        "iss": "executive-agent",
        "aud": "api",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    try:
        encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(
            "access_token_created",
            user_id=user_id,
            expires_in_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
            roles=roles
        )
        return encoded_jwt
    except Exception as e:
        logger.error("access_token_creation_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create authentication token"
        )


def create_refresh_token(user_id: str) -> str:
    """
    Create JWT refresh token (longer expiration)

    Args:
        user_id: Unique user identifier

    Returns:
        Refresh token string
    """
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    token_data = {
        "sub": user_id,
        "type": "refresh",
        "iss": "executive-agent",
        "aud": "api",
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int(expire.timestamp()),
    }

    try:
        encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        logger.info("refresh_token_created", user_id=user_id)
        return encoded_jwt
    except Exception as e:
        logger.error("refresh_token_creation_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create refresh token"
        )


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserContext:
    """
    Verify JWT token and extract user context

    Args:
        credentials: HTTP Bearer token from request header

    Returns:
        UserContext with user information and permissions

    Raises:
        HTTPException: If token is invalid, expired, or missing
    """
    if not credentials:
        logger.warning("auth_missing_credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience="api",
            issuer="executive-agent",
        )

        # Verify token type (not refresh token)
        if payload.get("type") == "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cannot use refresh token for API access"
            )

        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning("auth_token_missing_subject")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        issued_at = datetime.fromtimestamp(payload.get("iat", 0), tz=timezone.utc)
        expires_at = datetime.fromtimestamp(payload.get("exp", 0), tz=timezone.utc)

        user_context = UserContext(
            user_id=user_id,
            email=payload.get("email"),
            roles=payload.get("roles", ["user"]),
            permissions=payload.get("permissions", []),
            issued_at=issued_at,
            expires_at=expires_at
        )

        logger.info("auth_token_verified", user_id=user_id, roles=user_context.roles)
        return user_context

    except ExpiredSignatureError:
        logger.warning("auth_token_expired", token_preview=token[:20])
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired"
        )
    except JWTError as e:
        logger.warning("auth_invalid_token", error=str(e), token_preview=token[:20])
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    except Exception as e:
        logger.error("auth_verification_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication verification failed"
        )


def require_role(required_roles: list[str]):
    """
    Dependency for role-based access control

    Usage:
        @router.post("/admin/endpoint")
        async def admin_only(user: UserContext = Depends(require_role(["admin"]))):
            ...

    Args:
        required_roles: List of acceptable roles

    Returns:
        Dependency function that validates user roles
    """
    async def role_checker(user: UserContext = Depends(verify_token)) -> UserContext:
        if not any(role in user.roles for role in required_roles):
            logger.warning(
                "auth_insufficient_permissions",
                user_id=user.user_id,
                required_roles=required_roles,
                user_roles=user.roles
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {required_roles}"
            )
        return user

    return role_checker


def require_permission(required_permissions: list[str]):
    """
    Dependency for permission-based access control

    Args:
        required_permissions: List of required permissions

    Returns:
        Dependency function that validates permissions
    """
    async def permission_checker(user: UserContext = Depends(verify_token)) -> UserContext:
        if not any(perm in user.permissions for perm in required_permissions):
            logger.warning(
                "auth_insufficient_permissions",
                user_id=user.user_id,
                required_permissions=required_permissions,
                user_permissions=user.permissions
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {required_permissions}"
            )
        return user

    return permission_checker
