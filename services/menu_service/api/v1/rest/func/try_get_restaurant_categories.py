from sqlalchemy.orm import Session
import uuid
from utility.db import SessionLocal
from schemas.common import ResultDto, create_success_result, create_error_result


async def try_get_restaurant_categories(restaurant_id: uuid.UUID) -> ResultDto:
    """해당 매장의 메뉴 카테고리 조회 - 메뉴 필터 탭 또는 스크롤 고정 영역 구성 시"""
    db = SessionLocal()
    try:
        from model.menu import MenuCategory
        
        categories = db.query(MenuCategory)\
            .filter(MenuCategory.restaurant_id == restaurant_id)\
            .filter(MenuCategory.is_deleted == False)\
            .order_by(MenuCategory.ordering)\
            .all()
        
        if not categories:
            return create_success_result([])
        
        result_data = [{
            "uuid": str(category.uuid),
            "restaurant_id": str(category.restaurant_id),
            "name": category.name,
            "ordering": category.ordering
        } for category in categories]
        
        return create_success_result(result_data)
        
    except Exception as e:
        return create_error_result(e)
    finally:
        db.close()