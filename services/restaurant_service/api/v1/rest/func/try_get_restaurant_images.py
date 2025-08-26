import uuid
from sqlalchemy.orm import Session
from model.restaurant import Restaurant, RestaurantImage
from schemas.response.restaurant import RestaurantImagesResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import RestaurantNotFoundException
from utility.db import get_db

async def try_get_restaurant_images(restaurant_id: uuid.UUID):
    """매장 이미지 리스트 조회"""
    session = next(get_db())
    
    try:
        # 먼저 매장이 존재하는지 확인
        restaurant = session.query(Restaurant).filter(
            Restaurant.uuid == restaurant_id,
            Restaurant.is_deleted == False
        ).first()
        
        if not restaurant:
            raise RestaurantNotFoundException(f"매장 ID {restaurant_id}를 찾을 수 없습니다")
        
        # 매장 이미지 조회 (없어도 빈 리스트로 반환)
        images = session.query(RestaurantImage).filter(
            RestaurantImage.restaurant_id == restaurant_id,
            RestaurantImage.is_deleted == False
        ).order_by(RestaurantImage.ordering.asc()).all()
        
        return RestaurantImagesResponseDto.create_result(images)
        
    except RestaurantNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close()