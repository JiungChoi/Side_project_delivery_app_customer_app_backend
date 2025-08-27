# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from schemas.request.delete_review import DeleteReviewRequestDto
from schemas.response.delete_review import DeleteReviewResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    AuthenticationException,
    ReviewNotFoundException,
    ReviewPermissionException
)
from model.review import Review
from utility.db import get_db
from uuid import UUID
from datetime import datetime


async def try_delete_review(review_id: UUID, request: DeleteReviewRequestDto):
    session = next(get_db())
    
    try:
        if not request.user_id:
            raise AuthenticationException("사용자 ID가 필요합니다.")

        # 리뷰 조회
        review = session.query(Review).filter(
            Review.uuid == review_id,
            Review.is_deleted == False
        ).first()

        if not review:
            raise ReviewNotFoundException("리뷰를 찾을 수 없습니다.")

        # 작성자 권한 확인
        if review.user_id != request.user_id:
            raise ReviewPermissionException("본인이 작성한 리뷰만 삭제할 수 있습니다.")

        # 리뷰 soft delete
        deleted_time = datetime.utcnow()
        review.is_deleted = True
        review.updated_at = deleted_time

        session.commit()

        response = DeleteReviewResponseDto(deleted_at=deleted_time)
        return create_success_result(response)
        
    except (AuthenticationException, ReviewNotFoundException, ReviewPermissionException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()