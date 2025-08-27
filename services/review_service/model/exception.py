# -*- coding: utf-8 -*-
"""
Review Service Exception Classes
이 모듈은 review_service에서 사용되는 모든 예외 클래스들을 정의함.
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


class ReviewServiceException(WCSException):
    """리뷰 서비스 기본 예외"""
    code = "PTCM-E300"
    name = "ReviewServiceException"

    def __init__(self, message: str = "리뷰 서비스 예외가 발생했습니다"):
        super().__init__(message)


class ReviewNotFoundException(ReviewServiceException):
    """리뷰를 찾을 수 없음"""
    code = "PTCM-E301"
    name = "ReviewNotFoundException"

    def __init__(self, message: str = "리뷰를 찾을 수 없습니다"):
        super().__init__(message)


class ReviewValidationException(ReviewServiceException):
    """리뷰 검증 예외"""
    code = "PTCM-E302"
    name = "ReviewValidationException"

    def __init__(self, message: str = "리뷰 정보가 올바르지 않습니다"):
        super().__init__(message)


class ReviewPermissionException(ReviewServiceException):
    """리뷰 권한 예외"""
    code = "PTCM-E303"
    name = "ReviewPermissionException"

    def __init__(self, message: str = "리뷰에 대한 권한이 없습니다"):
        super().__init__(message)


class OrderNotFoundException(ReviewServiceException):
    """주문을 찾을 수 없음"""
    code = "PTCM-E304"
    name = "OrderNotFoundException"

    def __init__(self, message: str = "주문을 찾을 수 없습니다"):
        super().__init__(message)


class OrderNotCompletedException(ReviewServiceException):
    """주문이 완료되지 않음"""
    code = "PTCM-E305"
    name = "OrderNotCompletedException"

    def __init__(self, message: str = "완료되지 않은 주문에는 리뷰를 작성할 수 없습니다"):
        super().__init__(message)


class ReviewAlreadyExistsException(ReviewServiceException):
    """이미 리뷰가 존재함"""
    code = "PTCM-E306"
    name = "ReviewAlreadyExistsException"

    def __init__(self, message: str = "해당 주문에 대한 리뷰가 이미 존재합니다"):
        super().__init__(message)


class RestaurantNotFoundException(ReviewServiceException):
    """매장을 찾을 수 없음"""
    code = "PTCM-E307"
    name = "RestaurantNotFoundException"

    def __init__(self, message: str = "매장을 찾을 수 없습니다"):
        super().__init__(message)


class UserNotFoundException(ReviewServiceException):
    """사용자를 찾을 수 없음"""
    code = "PTCM-E308"
    name = "UserNotFoundException"

    def __init__(self, message: str = "사용자를 찾을 수 없습니다"):
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