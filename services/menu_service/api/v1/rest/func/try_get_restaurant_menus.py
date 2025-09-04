from sqlalchemy.orm import Session
import uuid
from utility.db import SessionLocal
from schemas.common import ResultDto, create_success_result, create_error_result


async def try_get_restaurant_menus(restaurant_id: uuid.UUID) -> ResultDto:
    """특정 매장의 전체 메뉴 조회 - 매장 상세 페이지 진입 시, 메뉴 탭 로딩 시"""
    db = SessionLocal()
    try:
        from model.menu import MenuCategory
        
        print(f"[MENU_SERVICE] Searching menus for restaurant_id: {restaurant_id}")
        
        categories = db.query(MenuCategory)\
            .filter(MenuCategory.restaurant_id == restaurant_id)\
            .filter(MenuCategory.is_deleted == False)\
            .order_by(MenuCategory.ordering)\
            .all()
        
        print(f"[MENU_SERVICE] Found {len(categories)} categories for restaurant {restaurant_id}")
        
        if not categories:
            print(f"[MENU_SERVICE] No categories found for restaurant {restaurant_id}, returning empty array")
            return create_success_result([])
        
        result_data = []
        for category in categories:
            print(f"[MENU_SERVICE] Processing category: {category.name} (uuid: {category.uuid})")
            active_menus = [menu for menu in category.menus if not menu.is_deleted]
            print(f"[MENU_SERVICE] Category '{category.name}' has {len(active_menus)} active menus")
            
            category_data = {
                "uuid": str(category.uuid),
                "restaurant_id": str(category.restaurant_id),
                "name": category.name,
                "ordering": category.ordering,
                "menus": [{
                    "uuid": str(menu.uuid),
                    "category_id": str(menu.category_id),
                    "name": menu.name,
                    "description": menu.description,
                    "price": menu.price,
                    "image_url": menu.image_url,
                    "is_sold_out": menu.is_sold_out,
                    "ordering": menu.ordering
                } for menu in active_menus]
            }
            result_data.append(category_data)
        
        print(f"[MENU_SERVICE] Returning {len(result_data)} categories with total menus")
        return create_success_result(result_data)
        
    except Exception as e:
        print(f"[MENU_SERVICE] Error getting restaurant menus: {e}")
        return create_error_result(e)
    finally:
        db.close()