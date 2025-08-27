# -*- coding: utf-8 -*-
"""
Customer Support API Router

고객지원 관련 API 엔드포인트들을 정의합니다.
"""

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

# Request/Response DTOs
from schemas.request.create_support import CreateSupportRequestDto
from schemas.request.get_my_supports import GetMySupportsRequestDto
from schemas.request.get_support_detail import GetSupportDetailRequestDto

from schemas.response.create_support import CreateSupportResponseDto
from schemas.response.get_my_supports import GetMySupportsResponseDto
from schemas.response.get_support_detail import GetSupportDetailResponseDto

# Common schemas
from schemas.common import (
    ResultDto,
    create_success_result,
    create_error_result,
    create_unknown_error_result
)

# Business logic functions
from api.v1.rest.func.try_create_support import try_create_support
from api.v1.rest.func.try_get_my_supports import try_get_my_supports
from api.v1.rest.func.try_get_support_detail import try_get_support_detail

# Database
from utility.db import get_db

# Exceptions
from model.exception import WCSException

from utility.logger import logger

router = APIRouter()


@router.post("/supports", status_code=status.HTTP_201_CREATED, response_model=ResultDto[CreateSupportResponseDto])
def create_support(
    request: CreateSupportRequestDto,
    db: Session = Depends(get_db)
):
    """
    1:1 문의 등록
    
    고객이 앱에서 문의 유형, 제목, 내용을 작성하고 "문의 등록" 버튼을 눌렀을 때 호출
    """
    try:
        result = try_create_support(db, request)
        return create_success_result(result)
    except WCSException as e:
        logger.warning(f"문의 등록 실패: {e.message}")
        return create_error_result(e)
    except Exception as e:
        logger.error(f"문의 등록 중 예상치 못한 오류: {str(e)}")
        return create_unknown_error_result(e)


@router.get("/supports/my", status_code=status.HTTP_200_OK, response_model=ResultDto[GetMySupportsResponseDto])
def get_my_supports(
    user_id: UUID = Query(..., description="사용자 ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="문의 상태 필터"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(10, ge=1, le=100, description="페이지 크기"),
    db: Session = Depends(get_db)
):
    """
    내가 등록한 1:1 문의 목록 조회
    
    마이페이지 > 고객센터 > 나의 문의 내역 진입 시 호출
    """
    try:
        request = GetMySupportsRequestDto(
            user_id=user_id,
            status=status_filter,
            page=page,
            size=size
        )
        result = try_get_my_supports(db, request)
        return create_success_result(result)
    except WCSException as e:
        logger.warning(f"문의 목록 조회 실패: {e.message}")
        return create_error_result(e)
    except Exception as e:
        logger.error(f"문의 목록 조회 중 예상치 못한 오류: {str(e)}")
        return create_unknown_error_result(e)


@router.get("/supports/{support_id}", status_code=status.HTTP_200_OK, response_model=ResultDto[GetSupportDetailResponseDto])
def get_support_detail(
    support_id: UUID,
    user_id: UUID = Query(..., description="사용자 ID"),
    db: Session = Depends(get_db)
):
    """
    특정 문의 상세 조회 (운영자 답변 포함)
    
    고객이 문의 내역을 클릭해 상세 보기 진입 시 호출
    """
    try:
        request = GetSupportDetailRequestDto(
            support_id=support_id,
            user_id=user_id
        )
        result = try_get_support_detail(db, request)
        return create_success_result(result)
    except WCSException as e:
        logger.warning(f"문의 상세 조회 실패: {e.message}")
        return create_error_result(e)
    except Exception as e:
        logger.error(f"문의 상세 조회 중 예상치 못한 오류: {str(e)}")
        return create_unknown_error_result(e)