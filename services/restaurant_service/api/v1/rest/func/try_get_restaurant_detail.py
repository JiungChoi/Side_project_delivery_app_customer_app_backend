import uuid
from sqlalchemy.orm import Session
from model.restaurant import Restaurant
from schemas.response.restaurant import RestaurantDetailResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import RestaurantNotFoundException
from utility.db import get_db

async def try_get_restaurant_detail(restaurant_id: uuid.UUID):
    """특정 매장 상세정보 조회"""
    session = next(get_db())
    
    try:
        # 특정 매장 조회
        restaurant = session.query(Restaurant).filter(
            Restaurant.uuid == restaurant_id,
            Restaurant.is_deleted == False
        ).first()
        
        if not restaurant:
            raise RestaurantNotFoundException(f"매장 ID {restaurant_id}를 찾을 수 없습니다")
        
        return RestaurantDetailResponseDto.create_result(restaurant)
        
    except RestaurantNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close()