# -*- coding: utf-8 -*-
"""
Authentication Middleware for Gateway Service

Gateway에서 모든 요청에 대한 JWT 토큰 검증을 수행합니다.
"""

import httpx
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from config import Config
from utility.logger import logger
import jwt


async def auth_middleware(request: Request, call_next):
    """
    Gateway 인증 미들웨어

    1. Public endpoints 체크
    2. JWT 토큰 추출 및 검증
    3. 검증된 user_id를 백엔드 서비스로 전달
    """

    # Request path 정리
    path = str(request.url.path)
    method = request.method

    logger.info(f"[AUTH_MIDDLEWARE] {method} {path}")

    # 1. Public endpoints 체크
    if _is_public_endpoint(path, method):
        logger.info(f"[AUTH_MIDDLEWARE] Public endpoint, auth skipped: {path}")
        response = await call_next(request)
        return response

    # 2. Authorization 헤더에서 JWT 토큰 추출
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning(f"[AUTH_MIDDLEWARE] Missing or invalid Authorization header for {path}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Authentication required", "message": "Missing or invalid authorization header"}
        )

    token = auth_header.split("Bearer ")[1]

    # 3. JWT 토큰 검증
    try:
        user_info = await _verify_jwt_token(token)
        if not user_info:
            logger.warning(f"[AUTH_MIDDLEWARE] Invalid token for {path}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid token", "message": "Token verification failed"}
            )

        # 4. 검증된 사용자 정보를 헤더에 추가하여 백엔드 서비스로 전달
        user_id = user_info.get("user_id")
        user_role = user_info.get("role", "customer")

        # Request 객체에 커스텀 헤더 추가
        # 백엔드 서비스에서 X-User-ID, X-User-Role 헤더를 통해 인증된 사용자 정보 사용
        request.headers.__dict__["_list"].append(
            (b"x-user-id", str(user_id).encode())
        )
        request.headers.__dict__["_list"].append(
            (b"x-user-role", user_role.encode())
        )

        logger.info(f"[AUTH_MIDDLEWARE] Authentication successful - user_id: {user_id}, role: {user_role}")

        # 5. 인증된 요청을 백엔드 서비스로 전달
        response = await call_next(request)
        return response

    except jwt.ExpiredSignatureError:
        logger.warning(f"[AUTH_MIDDLEWARE] Expired token for {path}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Token expired", "message": "Token has expired, please login again"}
        )
    except jwt.InvalidTokenError as e:
        logger.warning(f"[AUTH_MIDDLEWARE] Invalid token for {path}: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid token", "message": "Token is invalid"}
        )
    except Exception as e:
        logger.error(f"[AUTH_MIDDLEWARE] Authentication error for {path}: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Authentication error", "message": "Internal authentication error"}
        )


def _is_public_endpoint(path: str, method: str) -> bool:
    """
    Public endpoint 여부 확인

    Args:
        path: Request path
        method: HTTP method

    Returns:
        bool: Public endpoint 여부
    """
    # Exact path matching
    if path in Config.PUBLIC_ENDPOINTS:
        return True

    # Pattern matching for dynamic paths
    public_patterns = [
        "/api/v1/rest/health",
        "/api/v1/rest/auth-service/",
        "/api/v1/rest/restaurant-service/restaurants",
        "/api/v1/rest/menu-service/restaurants",
        "/api/v1/rest/cart-service/"  # Cart service patterns (temporary until login implemented)
    ]

    for pattern in public_patterns:
        if path.startswith(pattern):
            return True

    return False


async def _verify_jwt_token(token: str) -> dict:
    """
    JWT 토큰 검증

    두 가지 방법으로 검증:
    1. 로컬에서 직접 JWT 검증 (빠름)
    2. Auth service를 통한 검증 (더 안전하지만 느림)

    Args:
        token: JWT token

    Returns:
        dict: 사용자 정보 또는 None
    """
    try:
        # 방법 1: 로컬에서 직접 JWT 검증 (권장)
        payload = jwt.decode(
            token,
            Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )

        # 토큰에서 사용자 정보 추출
        user_id = payload.get("user_id")
        user_role = payload.get("role", "customer")
        exp = payload.get("exp")

        if not user_id:
            logger.warning("[AUTH_MIDDLEWARE] Token missing user_id")
            return None

        logger.info(f"[AUTH_MIDDLEWARE] Token verified locally - user_id: {user_id}, exp: {exp}")
        return {
            "user_id": user_id,
            "role": user_role,
            "exp": exp
        }

    except jwt.ExpiredSignatureError:
        logger.warning("[AUTH_MIDDLEWARE] Token expired during local verification")
        raise
    except jwt.InvalidTokenError as e:
        logger.warning(f"[AUTH_MIDDLEWARE] Invalid token during local verification: {str(e)}")

        # 방법 2: Auth service를 통한 검증 (fallback)
        try:
            return await _verify_token_with_auth_service(token)
        except Exception as fallback_error:
            logger.error(f"[AUTH_MIDDLEWARE] Auth service verification also failed: {str(fallback_error)}")
            return None
    except Exception as e:
        logger.error(f"[AUTH_MIDDLEWARE] Unexpected error during token verification: {str(e)}")
        return None


async def _verify_token_with_auth_service(token: str) -> dict:
    """
    Auth service를 통한 토큰 검증 (fallback method)

    Args:
        token: JWT token

    Returns:
        dict: 사용자 정보 또는 None
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{Config.AUTH_SERVICE_INTERNAL_URL}/api/v1/rest/verify-token",
                json={"token": token},
                timeout=5.0
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("valid"):
                    user_info = result.get("user_info", {})
                    logger.info(f"[AUTH_MIDDLEWARE] Token verified by auth service - user_id: {user_info.get('user_id')}")
                    return user_info

            logger.warning(f"[AUTH_MIDDLEWARE] Auth service token verification failed: {response.status_code}")
            return None

    except httpx.TimeoutException:
        logger.error("[AUTH_MIDDLEWARE] Auth service verification timeout")
        return None
    except Exception as e:
        logger.error(f"[AUTH_MIDDLEWARE] Auth service verification error: {str(e)}")
        return None