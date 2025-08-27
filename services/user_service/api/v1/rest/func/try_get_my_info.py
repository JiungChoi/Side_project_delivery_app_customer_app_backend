# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from schemas.request.get_my_info import GetMyInfoRequestDto
from schemas.response.get_my_info import GetMyInfoResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    AuthenticationException, 
    UserNotFoundException
)
from model.user import User
from utility.db import get_db


async def try_get_my_info(request: GetMyInfoRequestDto):
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

        response = GetMyInfoResponseDto(
            user_id=user.uuid,
            email=user.email,
            phone=user.phone,
            name=user.name,
            profile_image_url=user.profile_image_url,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        return create_success_result(response)
        
    except (AuthenticationException, UserNotFoundException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()