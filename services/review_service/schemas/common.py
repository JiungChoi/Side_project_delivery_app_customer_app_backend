# -*- coding: utf-8 -*-
from typing import Optional, Generic, TypeVar, Any
from pydantic import BaseModel, Field
from model.exception import (
    WCSException,
    ConnectionException,
    ReviewServiceException,
    ReviewNotFoundException,
    ReviewValidationException,
    ReviewPermissionException,
    OrderNotFoundException,
    OrderNotCompletedException,
    ReviewAlreadyExistsException,
    RestaurantNotFoundException,
    UserNotFoundException,
    DatabaseException,
    ExternalServiceException,
    AuthenticationException,
    AuthorizationException,
    UnknownException
)


# Pydantic 버전 (REST API용)
class ErrorDto(BaseModel):
    """에러 정보를 담는 Pydantic 모델"""
    code: str = Field(..., description="에러 코드")
    name: str = Field(..., description="에러 이름")
    message: str = Field(..., description="에러 메시지")


T = TypeVar("T")


class ResultDto(BaseModel, Generic[T]):
    """결과를 담는 Pydantic 모델 (성공/실패 통합)"""
    data: Optional[T] = Field(None, description="성공 데이터")
    error: Optional[ErrorDto] = Field(None, description="에러 정보")


# Result 생성 헬퍼 함수들
def create_success_result(data: Any) -> ResultDto:
    """성공 결과 생성"""
    return ResultDto(data=data)


def create_error_result(exception: WCSException) -> ResultDto:
    """에러 결과 생성"""
    error = ErrorDto(
        code=exception.code,
        name=exception.name,
        message=exception.message
    )
    return ResultDto(error=error)


def create_unknown_error_result(exception: Exception) -> ResultDto:
    """알 수 없는 에러 결과 생성"""
    error = ErrorDto(
        code="PTCM-E999",
        name="UnknownException",
        message=str(exception)
    )
    return ResultDto(error=error)


def try_get_data_from_result(result: dict) -> Any:
    """Result에서 데이터 추출 (에러 시 예외 발생)"""
    data = result.get('data')
    error = result.get('error')
    
    if data is not None:
        return data
    
    if error is not None:
        code = error.get('code')
        message = error.get('message', 'Unknown error')
        name = error.get('name', 'UnknownException')
        
        # 에러 코드에 따른 예외 생성
        if code == "PTCM-E000":
            raise WCSException(message)
        elif code == "PTCM-E001":
            raise ConnectionException(message)
        elif code == "PTCM-E300":
            raise ReviewServiceException(message)
        elif code == "PTCM-E301":
            raise ReviewNotFoundException(message)
        elif code == "PTCM-E302":
            raise ReviewValidationException(message)
        elif code == "PTCM-E303":
            raise ReviewPermissionException(message)
        elif code == "PTCM-E304":
            raise OrderNotFoundException(message)
        elif code == "PTCM-E305":
            raise OrderNotCompletedException(message)
        elif code == "PTCM-E306":
            raise ReviewAlreadyExistsException(message)
        elif code == "PTCM-E307":
            raise RestaurantNotFoundException(message)
        elif code == "PTCM-E308":
            raise UserNotFoundException(message)
        elif code == "PTCM-E500":
            raise DatabaseException(message)
        elif code == "PTCM-E600":
            raise ExternalServiceException(message)
        elif code == "PTCM-E700":
            raise AuthenticationException(message)
        elif code == "PTCM-E701":
            raise AuthorizationException(message)
        elif code == "PTCM-E999":
            raise UnknownException(message)
        else:
            raise WCSException(message)
    
    raise WCSException('No data or error in result')