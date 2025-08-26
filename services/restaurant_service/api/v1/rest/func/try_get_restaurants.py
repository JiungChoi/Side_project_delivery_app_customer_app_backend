from sqlalchemy.orm import Session
from model.restaurant import Restaurant
from schemas.response.restaurant import RestaurantsListResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import RestaurantNotFoundException
from utility.db import get_db

async def try_get_restaurants():
    """전체 매장 리스트 조회"""
    session = next(get_db())
    
    try:
        # 삭제되지 않은 매장들 조회
        restaurants = session.query(Restaurant).filter(Restaurant.is_deleted == False).all()
        
        # 매장이 없는 경우는 빈 리스트로 반환 (오류가 아님)
        return RestaurantsListResponseDto.create_result(restaurants)
        
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close()