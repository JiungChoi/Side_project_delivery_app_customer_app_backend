"""
Cart Service Exception Classes
이 모듈은 cart_service에서 사용되는 모든 예외 클래스들을 정의함.
"""


class WCSException(Exception):
    """WCS 기본 예외 클래스"""
    code = "PTCM-E000"
    name = "WCSException"

    def __init__(self, message: str = "WCS 기본 예외가 발생했습니다"):
        self.message = message
        super().__init__(self.message)


class ConnectionException(WCSException):
    """연결 관련 예외"""
    code = "PTCM-E001"
    name = "ConnectionException"

    def __init__(self, message: str = "연결에 실패했습니다"):
        super().__init__(message)


class CartServiceException(WCSException):
    """장바구니 서비스 기본 예외"""
    code = "PTCM-E200"
    name = "CartServiceException"

    def __init__(self, message: str = "장바구니 서비스 예외가 발생했습니다"):
        super().__init__(message)


class CartNotFoundException(CartServiceException):
    """장바구니를 찾을 수 없음"""
    code = "PTCM-E201"
    name = "CartNotFoundException"

    def __init__(self, message: str = "장바구니를 찾을 수 없습니다"):
        super().__init__(message)


class CartItemNotFoundException(CartServiceException):
    """장바구니 항목을 찾을 수 없음"""
    code = "PTCM-E202"
    name = "CartItemNotFoundException"

    def __init__(self, message: str = "장바구니 항목을 찾을 수 없습니다"):
        super().__init__(message)


class CartValidationException(CartServiceException):
    """장바구니 검증 예외"""
    code = "PTCM-E203"
    name = "CartValidationException"

    def __init__(self, message: str = "장바구니 정보가 올바르지 않습니다"):
        super().__init__(message)


class RestaurantMismatchException(CartServiceException):
    """다른 매장 메뉴 추가 시도"""
    code = "PTCM-E204"
    name = "RestaurantMismatchException"

    def __init__(self, message: str = "다른 매장의 메뉴는 장바구니에 추가할 수 없습니다"):
        super().__init__(message)


class MenuNotFoundException(CartServiceException):
    """메뉴를 찾을 수 없음"""
    code = "PTCM-E205"
    name = "MenuNotFoundException"

    def __init__(self, message: str = "메뉴를 찾을 수 없습니다"):
        super().__init__(message)


class UserNotFoundException(CartServiceException):
    """사용자를 찾을 수 없음"""
    code = "PTCM-E206"
    name = "UserNotFoundException"

    def __init__(self, message: str = "사용자를 찾을 수 없습니다"):
        super().__init__(message)


class CartItemValidationException(CartServiceException):
    """장바구니 항목 검증 예외"""
    code = "PTCM-E207"
    name = "CartItemValidationException"

    def __init__(self, message: str = "장바구니 항목 정보가 올바르지 않습니다"):
        super().__init__(message)


class DatabaseException(WCSException):
    """데이터베이스 관련 예외"""
    code = "PTCM-E500"
    name = "DatabaseException"

    def __init__(self, message: str = "데이터베이스 오류가 발생했습니다"):
        super().__init__(message)


class ExternalServiceException(WCSException):
    """외부 서비스 호출 관련 예외"""
    code = "PTCM-E600"
    name = "ExternalServiceException"

    def __init__(self, message: str = "외부 서비스 호출 중 오류가 발생했습니다"):
        super().__init__(message)


class AuthenticationException(WCSException):
    """인증 관련 예외"""
    code = "PTCM-E700"
    name = "AuthenticationException"

    def __init__(self, message: str = "인증에 실패했습니다"):
        super().__init__(message)


class AuthorizationException(WCSException):
    """권한 관련 예외"""
    code = "PTCM-E701"
    name = "AuthorizationException"

    def __init__(self, message: str = "권한이 없습니다"):
        super().__init__(message)


class UnknownException(WCSException):
    """알 수 없는 예외"""
    code = "PTCM-E999"
    name = "UnknownException"

    def __init__(self, message: str = "알 수 없는 오류가 발생했습니다"):
        super().__init__(message)