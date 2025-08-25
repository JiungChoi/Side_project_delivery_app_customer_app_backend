from sqlalchemy.orm import Session
import uuid
from utility.db import SessionLocal
from schemas.common import ResultDto, create_success_result, create_error_result
from model.exception import MenuNotFoundException


async def try_get_menu_options(menu_id: uuid.UUID) -> ResultDto:
    """해당 메뉴에 포함된 옵션 그룹 및 옵션 목록 조회 - 메뉴 상세 팝업 진입 시, 옵션 선택 영역 구성 시"""
    db = SessionLocal()
    try:
        from model.menu import Menu, MenuOptionGroup
        
        # 먼저 메뉴가 존재하는지 확인
        menu = db.query(Menu)\
            .filter(Menu.uuid == menu_id)\
            .filter(Menu.is_deleted == False)\
            .first()
        
        if not menu:
            raise MenuNotFoundException()
        
        # 메뉴 옵션 그룹들 조회
        option_groups = db.query(MenuOptionGroup)\
            .filter(MenuOptionGroup.menu_id == menu_id)\
            .filter(MenuOptionGroup.is_deleted == False)\
            .order_by(MenuOptionGroup.ordering)\
            .all()
        
        result_data = [{
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
        } for group in option_groups]
        
        return create_success_result(result_data)
        
    except MenuNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_error_result(e)
    finally:
        db.close()