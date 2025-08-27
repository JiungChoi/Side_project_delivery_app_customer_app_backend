# -*- coding: utf-8 -*-
"""
Customer Support Service Exception Classes
이 모듈은 customer_support_service에서 사용되는 모든 예외 클래스들을 정의함.
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


class CustomerSupportServiceException(WCSException):
    """고객지원 서비스 기본 예외"""
    code = "PTCM-E100"
    name = "CustomerSupportServiceException"

    def __init__(self, message: str = "고객지원 서비스 예외가 발생했습니다"):
        super().__init__(message)


class SupportRequestNotFoundException(CustomerSupportServiceException):
    """문의를 찾을 수 없음"""
    code = "PTCM-E101"
    name = "SupportRequestNotFoundException"

    def __init__(self, message: str = "문의를 찾을 수 없습니다"):
        super().__init__(message)


class SupportRequestValidationException(CustomerSupportServiceException):
    """문의 정보 검증 예외"""
    code = "PTCM-E102"
    name = "SupportRequestValidationException"

    def __init__(self, message: str = "문의 정보가 올바르지 않습니다"):
        super().__init__(message)


class SupportRequestPermissionException(CustomerSupportServiceException):
    """문의 권한 예외"""
    code = "PTCM-E103"
    name = "SupportRequestPermissionException"

    def __init__(self, message: str = "문의에 대한 권한이 없습니다"):
        super().__init__(message)


class SupportRequestStatusException(CustomerSupportServiceException):
    """문의 상태 예외"""
    code = "PTCM-E104"
    name = "SupportRequestStatusException"

    def __init__(self, message: str = "문의 상태가 올바르지 않습니다"):
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


class UnknownException(WCSException):
    """알 수 없는 예외"""
    code = "PTCM-E999"
    name = "UnknownException"

    def __init__(self, message: str = "알 수 없는 오류가 발생했습니다"):
        super().__init__(message)