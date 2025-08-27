# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from schemas.request.create_review import CreateReviewRequestDto
from schemas.response.create_review import CreateReviewResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    AuthenticationException, 
    ReviewValidationException,
    OrderNotFoundException,
    OrderNotCompletedException,
    ReviewAlreadyExistsException
)
from model.review import Review
from utility.db import get_db
from utility.enums import ReviewStatus
from uuid import uuid4
from datetime import datetime


async def try_create_review(request: CreateReviewRequestDto):
    session = next(get_db())
    
    try:
        if not request.user_id:
            raise AuthenticationException("사용자 ID가 필요합니다.")

        if not request.order_id:
            raise ReviewValidationException("주문 ID가 필요합니다.")

        if not request.restaurant_id:
            raise ReviewValidationException("매장 ID가 필요합니다.")

        if not (1 <= request.rating <= 5):
            raise ReviewValidationException("평점은 1-5 사이의 값이어야 합니다.")

        # 기존 리뷰 존재 여부 확인
        existing_review = session.query(Review).filter(
            Review.user_id == request.user_id,
            Review.order_id == request.order_id,
            Review.is_deleted == False
        ).first()

        if existing_review:
            raise ReviewAlreadyExistsException("해당 주문에 대한 리뷰가 이미 존재합니다.")

        # TODO: 주문 완료 상태 확인 - 실제 구현에서는 order_service 호출
        # order_status = get_order_status(request.order_id)
        # if order_status != "completed":
        #     raise OrderNotCompletedException("완료되지 않은 주문에는 리뷰를 작성할 수 없습니다.")

        # 리뷰 생성
        review = Review(
            uuid=uuid4(),
            user_id=request.user_id,
            order_id=request.order_id,
            restaurant_id=request.restaurant_id,
            rating=request.rating,
            content=request.content,
            image_url=request.image_url,
            status=ReviewStatus.ACTIVE.value
        )
        
        session.add(review)
        session.commit()

        response = CreateReviewResponseDto(
            review_id=review.uuid,
            created_at=review.created_at
        )
        return create_success_result(response)
        
    except (AuthenticationException, ReviewValidationException, OrderNotFoundException, 
            OrderNotCompletedException, ReviewAlreadyExistsException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()