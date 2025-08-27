# -*- coding: utf-8 -*-
"""
User Service Exception Classes
이 모듈은 user_service에서 사용되는 모든 예외 클래스들을 정의함.
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


class UserServiceException(WCSException):
    """사용자 서비스 기본 예외"""
    code = "PTCM-E100"
    name = "UserServiceException"

    def __init__(self, message: str = "사용자 서비스 예외가 발생했습니다"):
        super().__init__(message)


class UserNotFoundException(UserServiceException):
    """사용자를 찾을 수 없음"""
    code = "PTCM-E101"
    name = "UserNotFoundException"

    def __init__(self, message: str = "사용자를 찾을 수 없습니다"):
        super().__init__(message)


class UserValidationException(UserServiceException):
    """사용자 정보 검증 예외"""
    code = "PTCM-E102"
    name = "UserValidationException"

    def __init__(self, message: str = "사용자 정보가 올바르지 않습니다"):
        super().__init__(message)


class UserPermissionException(UserServiceException):
    """사용자 권한 예외"""
    code = "PTCM-E103"
    name = "UserPermissionException"

    def __init__(self, message: str = "사용자에 대한 권한이 없습니다"):
        super().__init__(message)


class DuplicateUserException(UserServiceException):
    """중복된 사용자 정보"""
    code = "PTCM-E104"
    name = "DuplicateUserException"

    def __init__(self, message: str = "이미 존재하는 사용자 정보입니다"):
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