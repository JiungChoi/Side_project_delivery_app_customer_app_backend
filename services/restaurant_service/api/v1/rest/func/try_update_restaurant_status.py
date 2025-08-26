import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func
from model.restaurant import Restaurant
from schemas.request.update_status import UpdateRestaurantStatusRequestDto
from schemas.response.restaurant import RestaurantStatusResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import RestaurantNotFoundException, RestaurantValidationException
from utility.db import get_db

async def try_update_restaurant_status(restaurant_id: uuid.UUID, request: UpdateRestaurantStatusRequestDto):
    """매장의 영업 상태 업데이트"""
    session = next(get_db())
    
    try:
        # 매장 조회
        restaurant = session.query(Restaurant).filter(
            Restaurant.uuid == restaurant_id,
            Restaurant.is_deleted == False
        ).first()
        
        if not restaurant:
            raise RestaurantNotFoundException(f"매장 ID {restaurant_id}를 찾을 수 없습니다")
        
        # 이전 상태 저장
        prev_status = restaurant.status
        new_status = request.status.value
        
        # 동일한 상태로 업데이트하려는 경우 체크
        if prev_status == new_status:
            raise RestaurantValidationException(f"매장 상태가 이미 '{new_status}'입니다")
        
        # 상태 업데이트
        restaurant.status = new_status
        restaurant.updated_at = func.now()
        
        session.commit()
        session.refresh(restaurant)
        
        return RestaurantStatusResponseDto.create_result(
            restaurant_id=restaurant_id,
            prev_status=prev_status,
            new_status=new_status,
            updated_at=restaurant.updated_at
        )
        
    except (RestaurantNotFoundException, RestaurantValidationException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()