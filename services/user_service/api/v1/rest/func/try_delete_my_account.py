# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from schemas.request.delete_my_account import DeleteMyAccountRequestDto
from schemas.response.delete_my_account import DeleteMyAccountResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    AuthenticationException, 
    UserNotFoundException,
    UserPermissionException
)
from model.user import User
from utility.db import get_db
from utility.enums import UserStatus
from datetime import datetime


async def try_delete_my_account(request: DeleteMyAccountRequestDto):
    session = next(get_db())
    
    try:
        if not request.user_id:
            raise AuthenticationException("사용자 ID가 필요합니다.")

        # 사용자 조회
        user = session.query(User).filter(
            User.uuid == request.user_id,
            User.is_deleted == False
        ).first()

        if not user:
            raise UserNotFoundException("사용자를 찾을 수 없습니다.")

        # 사용자 soft delete
        user.status = UserStatus.DELETED.value
        user.is_deleted = True
        user.updated_at = datetime.utcnow()
        
        session.commit()

        response = DeleteMyAccountResponseDto(
            deleted_at=user.updated_at
        )
        return create_success_result(response)
        
    except (AuthenticationException, UserNotFoundException, UserPermissionException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()