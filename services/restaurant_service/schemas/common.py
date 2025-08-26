# -*- coding: utf-8 -*-
from typing import Optional, TypeVar, Generic
from pydantic import BaseModel
from model.exception import *

T = TypeVar('T')

class ErrorDto(BaseModel):
    code: str
    name: str
    message: str

class ResultDto(BaseModel, Generic[T]):
    data: Optional[T] = None
    error: Optional[ErrorDto] = None

def create_success_result(data: T) -> ResultDto[T]:
    """성공 결과를 생성합니다."""
    return ResultDto(data=data, error=None)

def create_error_result(exception: Exception) -> ResultDto:
    """예외로부터 에러 결과를 생성합니다."""
    if hasattr(exception, 'code') and hasattr(exception, 'name'):
        error = ErrorDto(
            code=exception.code,
            name=exception.name,
            message=str(exception)
        )
    else:
        error = ErrorDto(
            code="PTCM-E999",
            name="UnknownException",
            message=str(exception)
        )
    
    return ResultDto(data=None, error=error)

def create_unknown_error_result(exception: Exception) -> ResultDto:
    """알 수 없는 예외로부터 에러 결과를 생성합니다."""
    error = ErrorDto(
        code="PTCM-E999",
        name="UnknownException",
        message=str(exception)
    )
    return ResultDto(data=None, error=error)

def try_get_data_from_result(result: ResultDto[T]) -> T:
    """ResultDto에서 데이터를 추출하거나 예외를 발생시킵니다."""
    if result.error:
        code = result.error.code
        message = result.error.message
        
        # 음식점 서비스 예외들
        if code == "PTCM-E121":
            raise RestaurantNotFoundException(message)
        elif code == "PTCM-E122":
            raise RestaurantValidationException(message)
        elif code == "PTCM-E123":
            raise RestaurantStatusException(message)
        elif code == "PTCM-E124":
            raise MenuNotFoundException(message)
        elif code == "PTCM-E125":
            raise CategoryNotFoundException(message)
        elif code == "PTCM-E126":
            raise ImageNotFoundException(message)
        # 공통 예외들
        elif code == "PTCM-E001":
            raise ConnectionException(message)
        elif code == "PTCM-E200":
            raise DatabaseException(message)
        elif code == "PTCM-E300":
            raise ExternalServiceException(message)
        elif code == "PTCM-E400":
            raise AuthenticationException(message)
        elif code == "PTCM-E401":
            raise AuthorizationException(message)
        elif code == "PTCM-E429":
            raise RateLimitException(message)
        else:
            raise UnknownException(message)
    
    return result.data