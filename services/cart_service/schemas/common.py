from typing import Optional, Generic, TypeVar, Any
from pydantic import BaseModel, Field
from model.exception import (
    WCSException,
    ConnectionException,
    CartServiceException,
    CartNotFoundException,
    CartItemNotFoundException,
    CartValidationException,
    RestaurantMismatchException,
    MenuNotFoundException,
    UserNotFoundException,
    CartItemValidationException,
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
        elif code == "PTCM-E200":
            raise CartServiceException(message)
        elif code == "PTCM-E201":
            raise CartNotFoundException(message)
        elif code == "PTCM-E202":
            raise CartItemNotFoundException(message)
        elif code == "PTCM-E203":
            raise CartValidationException(message)
        elif code == "PTCM-E204":
            raise RestaurantMismatchException(message)
        elif code == "PTCM-E205":
            raise MenuNotFoundException(message)
        elif code == "PTCM-E206":
            raise UserNotFoundException(message)
        elif code == "PTCM-E207":
            raise CartItemValidationException(message)
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