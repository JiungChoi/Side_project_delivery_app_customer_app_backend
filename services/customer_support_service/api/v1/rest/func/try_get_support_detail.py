# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from sqlalchemy import and_
from model.support_request import SupportRequest
from model.exception import (
    SupportRequestNotFoundException,
    SupportRequestPermissionException,
    DatabaseException
)
from schemas.request.get_support_detail import GetSupportDetailRequestDto
from schemas.response.get_support_detail import GetSupportDetailResponseDto
from utility.logger import logger


def try_get_support_detail(db: Session, request: GetSupportDetailRequestDto) -> GetSupportDetailResponseDto:
    """문의 상세 조회 (운영자 답변 포함)"""
    try:
        # 문의 조회
        support = db.query(SupportRequest).filter(
            and_(
                SupportRequest.uuid == request.support_id,
                SupportRequest.is_deleted == False
            )
        ).first()

        if not support:
            raise SupportRequestNotFoundException("해당 문의를 찾을 수 없습니다.")

        # 권한 확인 (본인의 문의만 조회 가능)
        if support.user_id != request.user_id:
            raise SupportRequestPermissionException("본인의 문의만 조회할 수 있습니다.")

        logger.info(f"문의 상세 조회 완료. ID: {request.support_id}, 사용자: {request.user_id}")

        return GetSupportDetailResponseDto(
            support_id=support.uuid,
            user_id=support.user_id,
            title=support.title,
            content=support.content,
            support_type=support.support_type,
            priority=support.priority,
            status=support.status,
            admin_response=support.admin_response,
            admin_id=support.admin_id,
            responded_at=support.responded_at,
            created_at=support.created_at,
            updated_at=support.updated_at
        )

    except Exception as e:
        if isinstance(e, (SupportRequestNotFoundException, SupportRequestPermissionException)):
            raise
        logger.error(f"문의 상세 조회 중 오류 발생: {str(e)}")
        raise DatabaseException("문의 상세 조회 중 데이터베이스 오류가 발생했습니다.")