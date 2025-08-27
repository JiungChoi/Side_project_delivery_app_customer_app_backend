# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from schemas.request.update_my_info import UpdateMyInfoRequestDto
from schemas.response.update_my_info import UpdateMyInfoResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    AuthenticationException, 
    UserNotFoundException,
    UserValidationException,
    DuplicateUserException
)
from model.user import User
from utility.db import get_db
from datetime import datetime


async def try_update_my_info(request: UpdateMyInfoRequestDto):
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

        # 전화번호 중복 확인
        if request.phone and request.phone != user.phone:
            existing_phone = session.query(User).filter(
                User.phone == request.phone,
                User.uuid != request.user_id,
                User.is_deleted == False
            ).first()
            if existing_phone:
                raise DuplicateUserException("이미 사용 중인 전화번호입니다.")

        # 사용자 정보 수정
        if request.name is not None:
            user.name = request.name
        if request.phone is not None:
            user.phone = request.phone
        if request.profile_image_url is not None:
            user.profile_image_url = request.profile_image_url
        
        user.updated_at = datetime.utcnow()
        session.commit()

        response = UpdateMyInfoResponseDto(
            updated_at=user.updated_at
        )
        return create_success_result(response)
        
    except (AuthenticationException, UserNotFoundException, UserValidationException, 
            DuplicateUserException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()