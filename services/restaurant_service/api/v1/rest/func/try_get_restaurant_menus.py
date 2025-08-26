import uuid
from sqlalchemy.orm import Session
from model.restaurant import Restaurant
from schemas.response.menu import RestaurantMenusResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import RestaurantNotFoundException, MenuNotFoundException
from utility.db import get_db

async def try_get_restaurant_menus(restaurant_id: uuid.UUID):
    """해당 매장의 메뉴 전체 리스트 조회"""
    session = next(get_db())
    
    try:
        # 먼저 매장이 존재하는지 확인
        restaurant = session.query(Restaurant).filter(
            Restaurant.uuid == restaurant_id,
            Restaurant.is_deleted == False
        ).first()
        
        if not restaurant:
            raise RestaurantNotFoundException(f"매장 ID {restaurant_id}를 찾을 수 없습니다")
        
        # TODO: 실제로는 menu_service에서 해당 매장의 메뉴 데이터를 가져와야 합니다
        # 현재는 임시로 빈 리스트를 반환합니다
        # 실제 구현 시에는 다음 방법들을 고려할 수 있습니다:
        # 1. menu_service API 호출 (HTTP 요청)
        # 2. 공유 데이터베이스 테이블 조회
        # 3. 메시지 큐를 통한 서비스 간 통신
        menus = []
        
        # 메뉴가 없어도 빈 리스트로 반환 (오류가 아님)
        return RestaurantMenusResponseDto.create_result(menus)
        
    except RestaurantNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close()