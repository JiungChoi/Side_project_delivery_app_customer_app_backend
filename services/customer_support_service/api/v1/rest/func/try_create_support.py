# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from model.support_request import SupportRequest
from model.exception import (
    SupportRequestValidationException,
    DatabaseException
)
from schemas.request.create_support import CreateSupportRequestDto
from schemas.response.create_support import CreateSupportResponseDto
from utility.enums import SupportStatus, SupportType, SupportPriority
from utility.logger import logger


def try_create_support(db: Session, request: CreateSupportRequestDto) -> CreateSupportResponseDto:
    """1:1 문의 등록"""
    try:
        # 유효성 검증
        if not request.title.strip():
            raise SupportRequestValidationException("문의 제목을 입력해주세요.")
        
        if not request.content.strip():
            raise SupportRequestValidationException("문의 내용을 입력해주세요.")
        
        # SupportType 검증
        valid_types = [e.value for e in SupportType]
        if request.support_type not in valid_types:
            raise SupportRequestValidationException(f"유효하지 않은 문의 유형입니다. 사용 가능한 유형: {', '.join(valid_types)}")
        
        # SupportPriority 검증
        valid_priorities = [e.value for e in SupportPriority]
        if request.priority not in valid_priorities:
            raise SupportRequestValidationException(f"유효하지 않은 우선순위입니다. 사용 가능한 우선순위: {', '.join(valid_priorities)}")

        # 새 문의 생성
        support_id = uuid.uuid4()
        new_support = SupportRequest(
            uuid=support_id,
            user_id=request.user_id,
            support_type=request.support_type,
            title=request.title.strip(),
            content=request.content.strip(),
            priority=request.priority,
            status=SupportStatus.PENDING.value
        )

        db.add(new_support)
        db.commit()
        db.refresh(new_support)

        logger.info(f"새 문의가 생성되었습니다. ID: {support_id}, 사용자: {request.user_id}")

        return CreateSupportResponseDto(
            support_id=new_support.uuid,
            title=new_support.title,
            support_type=new_support.support_type,
            status=new_support.status,
            created_at=new_support.created_at
        )

    except Exception as e:
        db.rollback()
        if isinstance(e, SupportRequestValidationException):
            raise
        logger.error(f"문의 생성 중 오류 발생: {str(e)}")
        raise DatabaseException("문의 생성 중 데이터베이스 오류가 발생했습니다.")