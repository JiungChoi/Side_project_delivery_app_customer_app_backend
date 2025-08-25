"""
Order Service Exception Classes
이 모듈은 order_service에서 사용되는 모든 예외 클래스들을 정의함.
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


class OrderServiceException(WCSException):
    """주문 서비스 기본 예외"""
    code = "PTCM-E100"
    name = "OrderServiceException"

    def __init__(self, message: str = "주문 서비스 예외가 발생했습니다"):
        super().__init__(message)


class OrderNotFoundException(OrderServiceException):
    """주문을 찾을 수 없음"""
    code = "PTCM-E101"
    name = "OrderNotFoundException"

    def __init__(self, message: str = "주문을 찾을 수 없습니다"):
        super().__init__(message)


class OrderStatusException(OrderServiceException):
    """주문 상태 관련 예외"""
    code = "PTCM-E102"
    name = "OrderStatusException"

    def __init__(self, message: str = "주문 상태 변경이 불가능합니다"):
        super().__init__(message)


class OrderValidationException(OrderServiceException):
    """주문 검증 예외"""
    code = "PTCM-E103"
    name = "OrderValidationException"

    def __init__(self, message: str = "주문 정보가 올바르지 않습니다"):
        super().__init__(message)


class PaymentException(OrderServiceException):
    """결제 관련 예외"""
    code = "PTCM-E104"
    name = "PaymentException"

    def __init__(self, message: str = "결제 처리 중 오류가 발생했습니다"):
        super().__init__(message)


class OrderItemException(OrderServiceException):
    """주문 아이템 관련 예외"""
    code = "PTCM-E105"
    name = "OrderItemException"

    def __init__(self, message: str = "주문 아이템 처리 중 오류가 발생했습니다"):
        super().__init__(message)


class RestaurantNotFoundException(OrderServiceException):
    """매장을 찾을 수 없음"""
    code = "PTCM-E106"
    name = "RestaurantNotFoundException"

    def __init__(self, message: str = "매장을 찾을 수 없습니다"):
        super().__init__(message)


class MenuNotFoundException(OrderServiceException):
    """메뉴를 찾을 수 없음"""
    code = "PTCM-E107"
    name = "MenuNotFoundException"

    def __init__(self, message: str = "메뉴를 찾을 수 없습니다"):
        super().__init__(message)


class AddressNotFoundException(OrderServiceException):
    """배송 주소를 찾을 수 없음"""
    code = "PTCM-E108"
    name = "AddressNotFoundException"

    def __init__(self, message: str = "배송 주소를 찾을 수 없습니다"):
        super().__init__(message)


class UserNotFoundException(OrderServiceException):
    """사용자를 찾을 수 없음"""
    code = "PTCM-E109"
    name = "UserNotFoundException"

    def __init__(self, message: str = "사용자를 찾을 수 없습니다"):
        super().__init__(message)


class OrderCancellationException(OrderServiceException):
    """주문 취소 관련 예외"""
    code = "PTCM-E110"
    name = "OrderCancellationException"

    def __init__(self, message: str = "주문 취소가 불가능합니다"):
        super().__init__(message)


class OrderCompletionException(OrderServiceException):
    """주문 완료 관련 예외"""
    code = "PTCM-E111"
    name = "OrderCompletionException"

    def __init__(self, message: str = "주문 완료 처리가 불가능합니다"):
        super().__init__(message)


class DatabaseException(WCSException):
    """데이터베이스 관련 예외"""
    code = "PTCM-E200"
    name = "DatabaseException"

    def __init__(self, message: str = "데이터베이스 오류가 발생했습니다"):
        super().__init__(message)


class ExternalServiceException(WCSException):
    """외부 서비스 호출 관련 예외"""
    code = "PTCM-E300"
    name = "ExternalServiceException"

    def __init__(self, message: str = "외부 서비스 호출 중 오류가 발생했습니다"):
        super().__init__(message)


class AuthenticationException(WCSException):
    """인증 관련 예외"""
    code = "PTCM-E400"
    name = "AuthenticationException"

    def __init__(self, message: str = "인증에 실패했습니다"):
        super().__init__(message)


class AuthorizationException(WCSException):
    """권한 관련 예외"""
    code = "PTCM-E401"
    name = "AuthorizationException"

    def __init__(self, message: str = "권한이 없습니다"):
        super().__init__(message)


class RateLimitException(WCSException):
    """요청 제한 관련 예외"""
    code = "PTCM-E429"
    name = "RateLimitException"

    def __init__(self, message: str = "요청 제한에 도달했습니다"):
        super().__init__(message)


class UnknownException(WCSException):
    """알 수 없는 예외"""
    code = "PTCM-E999"
    name = "UnknownException"

    def __init__(self, message: str = "알 수 없는 오류가 발생했습니다"):
        super().__init__(message) 