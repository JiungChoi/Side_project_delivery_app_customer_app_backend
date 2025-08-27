# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List
import math
from model.support_request import SupportRequest
from model.exception import DatabaseException
from schemas.request.get_my_supports import GetMySupportsRequestDto
from schemas.response.get_my_supports import GetMySupportsResponseDto, SupportSummaryDto
from utility.logger import logger


def try_get_my_supports(db: Session, request: GetMySupportsRequestDto) -> GetMySupportsResponseDto:
    """내 문의 목록 조회"""
    try:
        # 기본 쿼리 조건
        query_conditions = [
            SupportRequest.user_id == request.user_id,
            SupportRequest.is_deleted == False
        ]
        
        # 상태 필터 추가
        if request.status:
            query_conditions.append(SupportRequest.status == request.status)

        # 전체 개수 조회
        total_count = db.query(func.count(SupportRequest.uuid)).filter(
            and_(*query_conditions)
        ).scalar()

        # 페이징 계산
        offset = (request.page - 1) * request.size
        total_pages = math.ceil(total_count / request.size) if total_count > 0 else 0

        # 문의 목록 조회 (최신순 정렬)
        supports = db.query(SupportRequest).filter(
            and_(*query_conditions)
        ).order_by(
            SupportRequest.created_at.desc()
        ).offset(offset).limit(request.size).all()

        # DTO 변환
        support_dtos = []
        for support in supports:
            support_dtos.append(SupportSummaryDto(
                support_id=support.uuid,
                title=support.title,
                support_type=support.support_type,
                status=support.status,
                priority=support.priority,
                has_response=support.admin_response is not None,
                created_at=support.created_at,
                responded_at=support.responded_at
            ))

        logger.info(f"사용자 {request.user_id}의 문의 목록 조회 완료. 총 {total_count}건")

        return GetMySupportsResponseDto(
            supports=support_dtos,
            total_count=total_count,
            page=request.page,
            size=request.size,
            total_pages=total_pages
        )

    except Exception as e:
        logger.error(f"문의 목록 조회 중 오류 발생: {str(e)}")
        raise DatabaseException("문의 목록 조회 중 데이터베이스 오류가 발생했습니다.")