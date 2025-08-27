# -*- coding: utf-8 -*-
"""
User API Router

사용자 관련 API 엔드포인트들을 정의합니다.
"""

from fastapi import APIRouter, status, Query
from uuid import UUID
from typing import Optional

# Request/Response DTOs
from schemas.request.get_my_info import GetMyInfoRequestDto
from schemas.request.update_my_info import UpdateMyInfoRequestDto
from schemas.request.delete_my_account import DeleteMyAccountRequestDto
from schemas.request.check_exists import CheckExistsRequestDto

from schemas.response.get_my_info import GetMyInfoResponseDto
from schemas.response.update_my_info import UpdateMyInfoResponseDto
from schemas.response.delete_my_account import DeleteMyAccountResponseDto
from schemas.response.check_exists import CheckExistsResponseDto

# Common schemas
from schemas.common import (
    ResultDto,
    create_success_result,
    create_error_result,
    create_unknown_error_result
)

# Exception classes
from model.exception import (
    UserNotFoundException,
    UserValidationException,
    UserPermissionException,
    DuplicateUserException,
    AuthenticationException,
    AuthorizationException
)

# Business logic functions
from .func.try_get_my_info import try_get_my_info
from .func.try_update_my_info import try_update_my_info
from .func.try_delete_my_account import try_delete_my_account
from .func.try_check_exists import try_check_exists

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=ResultDto)
async def get_my_info(user_id: UUID):
    """
    내 정보 조회 API
    
    마이페이지 진입 시 호출됩니다.
    """
    try:
        request = GetMyInfoRequestDto(user_id=user_id)
        result = await try_get_my_info(request)
        return result
    except UserNotFoundException as e:
        return create_error_result(e)
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.patch("/me", response_model=ResultDto)
async def update_my_info(request: UpdateMyInfoRequestDto):
    """
    내 정보 수정 API
    
    고객이 이름, 전화번호 등 프로필 정보를 수정하고 저장할 때 호출됩니다.
    """
    try:
        result = await try_update_my_info(request)
        return result
    except UserNotFoundException as e:
        return create_error_result(e)
    except UserValidationException as e:
        return create_error_result(e)
    except DuplicateUserException as e:
        return create_error_result(e)
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.delete("/me", response_model=ResultDto)
async def delete_my_account(request: DeleteMyAccountRequestDto):
    """
    회원 탈퇴 요청 API
    
    고객이 "회원 탈퇴" 버튼을 눌렀을 때 호출됩니다.
    """
    try:
        result = await try_delete_my_account(request)
        return result
    except UserNotFoundException as e:
        return create_error_result(e)
    except UserPermissionException as e:
        return create_error_result(e)
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.get("/exists", response_model=ResultDto)
async def check_exists(
    email: Optional[str] = Query(None),
    phone: Optional[str] = Query(None)
):
    """
    이메일/전화번호 중복 확인 API
    
    회원가입 시 이메일 또는 전화번호 중복 여부 실시간 검사 시 호출됩니다.
    """
    try:
        request = CheckExistsRequestDto(email=email, phone=phone)
        result = await try_check_exists(request)
        return result
    except UserValidationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)