# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from schemas.request.check_exists import CheckExistsRequestDto
from schemas.response.check_exists import CheckExistsResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    UserValidationException
)
from model.user import User
from utility.db import get_db


async def try_check_exists(request: CheckExistsRequestDto):
    session = next(get_db())
    
    try:
        if not request.email and not request.phone:
            raise UserValidationException("이메일 또는 전화번호 중 하나는 필수입니다.")

        email_exists = False
        phone_exists = False

        # 이메일 중복 확인
        if request.email:
            existing_email = session.query(User).filter(
                User.email == request.email,
                User.is_deleted == False
            ).first()
            email_exists = existing_email is not None

        # 전화번호 중복 확인
        if request.phone:
            existing_phone = session.query(User).filter(
                User.phone == request.phone,
                User.is_deleted == False
            ).first()
            phone_exists = existing_phone is not None

        response = CheckExistsResponseDto(
            email_exists=email_exists,
            phone_exists=phone_exists
        )
        return create_success_result(response)
        
    except UserValidationException as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()