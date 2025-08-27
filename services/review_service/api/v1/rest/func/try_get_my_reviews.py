# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from schemas.request.get_my_reviews import GetMyReviewsRequestDto
from schemas.response.get_my_reviews import GetMyReviewsResponseDto, MyReviewDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import AuthenticationException
from model.review import Review
from utility.db import get_db
from utility.enums import ReviewStatus
from math import ceil


async def try_get_my_reviews(request: GetMyReviewsRequestDto):
    session = next(get_db())
    
    try:
        if not request.user_id:
            raise AuthenticationException("사용자 ID가 필요합니다.")

        # 사용자의 리뷰 조회
        query = session.query(Review).filter(
            Review.user_id == request.user_id,
            Review.status == ReviewStatus.ACTIVE.value,
            Review.is_deleted == False
        )

        # 전체 개수 조회
        total_count = query.count()

        # 페이징 적용
        offset = (request.page - 1) * request.limit
        reviews = query.order_by(Review.created_at.desc()).offset(offset).limit(request.limit).all()

        # 응답 DTO 생성
        review_dtos = [
            MyReviewDto(
                uuid=review.uuid,
                order_id=review.order_id,
                restaurant_id=review.restaurant_id,
                rating=review.rating,
                content=review.content,
                image_url=review.image_url,
                status=review.status,
                created_at=review.created_at,
                updated_at=review.updated_at
            )
            for review in reviews
        ]

        total_pages = ceil(total_count / request.limit) if total_count > 0 else 0

        response = GetMyReviewsResponseDto(
            reviews=review_dtos,
            total_count=total_count,
            page=request.page,
            limit=request.limit,
            total_pages=total_pages
        )
        return create_success_result(response)
        
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close()