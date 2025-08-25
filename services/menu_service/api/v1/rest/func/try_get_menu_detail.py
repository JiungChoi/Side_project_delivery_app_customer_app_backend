from sqlalchemy.orm import Session
import uuid
from utility.db import SessionLocal
from schemas.common import ResultDto, create_success_result, create_error_result
from model.exception import MenuNotFoundException


async def try_get_menu_detail(menu_id: uuid.UUID) -> ResultDto:
    """특정 메뉴 상세정보 조회 - 고객이 메뉴 항목을 터치해 상세 팝업을 열었을 때"""
    db = SessionLocal()
    try:
        from model.menu import Menu
        
        menu = db.query(Menu)\
            .filter(Menu.uuid == menu_id)\
            .filter(Menu.is_deleted == False)\
            .first()
        
        if not menu:
            raise MenuNotFoundException()
        
        result_data = {
            "uuid": str(menu.uuid),
            "category_id": str(menu.category_id),
            "name": menu.name,
            "description": menu.description,
            "price": menu.price,
            "image_url": menu.image_url,
            "is_sold_out": menu.is_sold_out,
            "ordering": menu.ordering,
            "option_groups": [{
                "uuid": str(group.uuid),
                "menu_id": str(group.menu_id),
                "name": group.name,
                "is_required": group.is_required,
                "max_select": group.max_select,
                "ordering": group.ordering,
                "options": [{
                    "uuid": str(option.uuid),
                    "group_id": str(option.group_id),
                    "name": option.name,
                    "price": option.price,
                    "ordering": option.ordering
                } for option in group.options if not option.is_deleted]
            } for group in menu.option_groups if not group.is_deleted]
        }
        
        return create_success_result(result_data)
        
    except MenuNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_error_result(e)
    finally:
        db.close()