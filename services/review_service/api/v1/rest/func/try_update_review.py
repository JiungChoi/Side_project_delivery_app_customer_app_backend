# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from schemas.request.update_review import UpdateReviewRequestDto
from schemas.response.update_review import UpdateReviewResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    AuthenticationException,
    ReviewNotFoundException,
    ReviewPermissionException,
    ReviewValidationException
)
from model.review import Review
from utility.db import get_db
from uuid import UUID
from datetime import datetime


async def try_update_review(review_id: UUID, request: UpdateReviewRequestDto):
    session = next(get_db())
    
    try:
        if not request.user_id:
            raise AuthenticationException("사용자 ID가 필요합니다.")

        if not (1 <= request.rating <= 5):
            raise ReviewValidationException("평점은 1-5 사이의 값이어야 합니다.")

        # 리뷰 조회
        review = session.query(Review).filter(
            Review.uuid == review_id,
            Review.is_deleted == False
        ).first()

        if not review:
            raise ReviewNotFoundException("리뷰를 찾을 수 없습니다.")

        # 작성자 권한 확인
        if review.user_id != request.user_id:
            raise ReviewPermissionException("본인이 작성한 리뷰만 수정할 수 있습니다.")

        # 리뷰 수정
        review.rating = request.rating
        review.content = request.content
        review.image_url = request.image_url
        review.updated_at = datetime.utcnow()

        session.commit()

        response = UpdateReviewResponseDto(updated_at=review.updated_at)
        return create_success_result(response)
        
    except (AuthenticationException, ReviewNotFoundException, ReviewPermissionException, ReviewValidationException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()