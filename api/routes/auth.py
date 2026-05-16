"""Authentication API endpoints - login, logout, token refresh"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
import structlog
from datetime import timedelta

from core.security.auth import (
    create_access_token,
    create_refresh_token,
    verify_token,
    UserContext,
)
from core.security.rbac import Role

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response with tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    roles: list[str]


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """New access token response"""
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Authenticate user and issue tokens

    NOTE: This is a placeholder implementation.
    In production, verify against your user database.

    For MVP testing:
    - username: "admin"
    - password: "admin" (returns admin role)

    - username: "operator"
    - password: "operator" (returns operator role)

    - username: "viewer"
    - password: "viewer" (returns viewer role)
    """
    try:
        # PLACEHOLDER: Replace with database verification
        known_users = {
            "admin": {
                "password": "admin",
                "email": "admin@executive-agent.local",
                "roles": [Role.ADMIN.value],
                "permissions": [],
            },
            "operator": {
                "password": "operator",
                "email": "operator@executive-agent.local",
                "roles": [Role.OPERATOR.value],
                "permissions": [],
            },
            "viewer": {
                "password": "viewer",
                "email": "viewer@executive-agent.local",
                "roles": [Role.VIEWER.value],
                "permissions": [],
            },
        }

        if request.username not in known_users:
            logger.warning("auth_login_failed_unknown_user", username=request.username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        user = known_users[request.username]
        if user["password"] != request.password:
            logger.warning("auth_login_failed_wrong_password", username=request.username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Create tokens
        user_id = request.username
        access_token = create_access_token(
            user_id=user_id,
            email=user["email"],
            roles=user["roles"],
            permissions=user["permissions"]
        )
        refresh_token = create_refresh_token(user_id)

        logger.info(
            "auth_login_success",
            user_id=user_id,
            roles=user["roles"]
        )

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
            roles=user["roles"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("auth_login_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh(request: RefreshTokenRequest):
    """
    Refresh access token using refresh token

    Args:
        RefreshTokenRequest: Contains refresh_token

    Returns:
        New access token
    """
    try:
        from jose import ExpiredSignatureError, JWTError, jwt
        from core.security.auth import ALGORITHM, SECRET_KEY

        # Decode refresh token
        payload = jwt.decode(
            request.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience="api",
            issuer="executive-agent",
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = payload.get("sub")

        # Create new access token (use same roles/permissions from original token)
        # In production, you'd fetch these from database
        access_token = create_access_token(
            user_id=user_id,
            roles=payload.get("roles", ["user"]),
            permissions=payload.get("permissions", [])
        )

        logger.info("auth_token_refreshed", user_id=user_id)

        return RefreshTokenResponse(
            access_token=access_token
        )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    except Exception as e:
        logger.error("auth_refresh_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/verify")
async def verify(user: UserContext = Depends(verify_token)):
    """
    Verify authentication and return user context

    This endpoint can be called without explicit credentials - the middleware
    will automatically verify the Bearer token if present.
    """
    return {
        "user_id": user.user_id,
        "email": user.email,
        "roles": user.roles,
        "permissions": user.permissions,
        "issued_at": user.issued_at.isoformat(),
        "expires_at": user.expires_at.isoformat(),
    }


@router.post("/logout")
async def logout(user: UserContext = Depends(verify_token)):
    """
    Logout endpoint (mostly symbolic - token invalidation should be handled client-side)

    In production, you might:
    - Add token to blacklist
    - Revoke refresh token
    - Clear session
    """
    logger.info("auth_logout", user_id=user.user_id)

    return {"message": "Logged out successfully"}
