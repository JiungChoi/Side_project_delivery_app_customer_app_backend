from sqlalchemy.orm import Session
from sqlalchemy import func, text
from model.restaurant import Restaurant
from schemas.response.restaurant import RestaurantsListResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import RestaurantNotFoundException
from utility.db import get_db

async def try_get_restaurants():
    """전체 매장 리스트 조회"""
    session = next(get_db())
    
    try:
        # 단순한 restaurant 테이블 직접 조회로 변경
        query = text("""
            SELECT 
                r.uuid,
                r.name,
                r.description,
                r.category,
                r.rating,
                r.review_count,
                r.min_order_amount,
                r.delivery_fee,
                r.delivery_time,
                r.operating_hours,
                r.tags,
                r.image_url,
                r.status,
                r.created_at,
                r.updated_at
            FROM restaurant_service.restaurant r
            WHERE r.is_deleted = false
            ORDER BY r.rating DESC, r.review_count DESC, r.created_at DESC
        """)
        
        result = session.execute(query).fetchall()
        
        # 결과를 Restaurant 객체 형태로 변환
        restaurants = []
        for row in result:
            restaurant = Restaurant(
                uuid=row.uuid,
                name=row.name, 
                description=row.description,
                category=row.category,
                rating=row.rating,  # DB에 저장된 값 직접 사용
                review_count=row.review_count,  # DB에 저장된 값 직접 사용
                min_order_amount=row.min_order_amount,
                delivery_fee=row.delivery_fee,
                delivery_time=row.delivery_time,
                operating_hours=row.operating_hours,
                tags=row.tags,
                image_url=row.image_url,
                status=row.status,
                created_at=row.created_at,
                updated_at=row.updated_at
            )
            restaurants.append(restaurant)
        
        # 매장이 없는 경우는 빈 리스트로 반환 (오류가 아님)
        return RestaurantsListResponseDto.create_result(restaurants)
        
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close()