# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas.request.get_restaurant_reviews import GetRestaurantReviewsRequestDto
from schemas.response.get_restaurant_reviews import GetRestaurantReviewsResponseDto, ReviewDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import RestaurantNotFoundException
from model.review import Review
from utility.db import get_db
from utility.enums import ReviewStatus
from uuid import UUID
from math import ceil


async def try_get_restaurant_reviews(restaurant_id: UUID, request: GetRestaurantReviewsRequestDto):
    session = next(get_db())
    
    try:
        if not restaurant_id:
            raise RestaurantNotFoundException("매장 ID가 필요합니다.")

        # 기본 쿼리
        query = session.query(Review).filter(
            Review.restaurant_id == restaurant_id,
            Review.status == ReviewStatus.ACTIVE.value,
            Review.is_deleted == False
        )

        # 평점 필터 적용
        if request.rating_filter:
            query = query.filter(Review.rating == request.rating_filter)

        # 전체 개수 조회
        total_count = query.count()

        # 평균 평점 계산
        avg_rating_result = session.query(func.avg(Review.rating)).filter(
            Review.restaurant_id == restaurant_id,
            Review.status == ReviewStatus.ACTIVE.value,
            Review.is_deleted == False
        ).scalar()
        
        average_rating = float(avg_rating_result) if avg_rating_result else 0.0

        # 페이징 적용
        offset = (request.page - 1) * request.limit
        reviews = query.order_by(Review.created_at.desc()).offset(offset).limit(request.limit).all()

        # 응답 DTO 생성
        review_dtos = [
            ReviewDto(
                uuid=review.uuid,
                user_id=review.user_id,
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

        response = GetRestaurantReviewsResponseDto(
            reviews=review_dtos,
            total_count=total_count,
            page=request.page,
            limit=request.limit,
            total_pages=total_pages,
            average_rating=round(average_rating, 2)
        )
        return create_success_result(response)
        
    except RestaurantNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close()