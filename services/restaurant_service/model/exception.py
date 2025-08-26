# -*- coding: utf-8 -*-

class WCSException(Exception):
    code = "PTCM-E000"
    name = "WCSException"
    
    def __init__(self, message: str = "시스템 오류가 발생했습니다"):
        super().__init__(message)
        self.message = message

class ConnectionException(WCSException):
    code = "PTCM-E001"
    name = "ConnectionException"
    
    def __init__(self, message: str = "연결 오류가 발생했습니다"):
        super().__init__(message)

class RestaurantServiceException(WCSException):
    code = "PTCM-E120"
    name = "RestaurantServiceException"
    
    def __init__(self, message: str = "음식점 서비스 오류가 발생했습니다"):
        super().__init__(message)

class RestaurantNotFoundException(RestaurantServiceException):
    code = "PTCM-E121"
    name = "RestaurantNotFoundException"
    
    def __init__(self, message: str = "음식점을 찾을 수 없습니다"):
        super().__init__(message)

class RestaurantValidationException(RestaurantServiceException):
    code = "PTCM-E122"
    name = "RestaurantValidationException"
    
    def __init__(self, message: str = "음식점 정보 검증에 실패했습니다"):
        super().__init__(message)

class RestaurantStatusException(RestaurantServiceException):
    code = "PTCM-E123"
    name = "RestaurantStatusException"
    
    def __init__(self, message: str = "음식점 상태 변경에 실패했습니다"):
        super().__init__(message)

class MenuNotFoundException(RestaurantServiceException):
    code = "PTCM-E124"
    name = "MenuNotFoundException"
    
    def __init__(self, message: str = "메뉴를 찾을 수 없습니다"):
        super().__init__(message)

class CategoryNotFoundException(RestaurantServiceException):
    code = "PTCM-E125"
    name = "CategoryNotFoundException"
    
    def __init__(self, message: str = "카테고리를 찾을 수 없습니다"):
        super().__init__(message)

class ImageNotFoundException(RestaurantServiceException):
    code = "PTCM-E126"
    name = "ImageNotFoundException"
    
    def __init__(self, message: str = "이미지를 찾을 수 없습니다"):
        super().__init__(message)

class DatabaseException(WCSException):
    code = "PTCM-E200"
    name = "DatabaseException"
    
    def __init__(self, message: str = "데이터베이스 오류가 발생했습니다"):
        super().__init__(message)

class ExternalServiceException(WCSException):
    code = "PTCM-E300"
    name = "ExternalServiceException"
    
    def __init__(self, message: str = "외부 서비스 오류가 발생했습니다"):
        super().__init__(message)

class AuthenticationException(WCSException):
    code = "PTCM-E400"
    name = "AuthenticationException"
    
    def __init__(self, message: str = "인증에 실패했습니다"):
        super().__init__(message)

class AuthorizationException(WCSException):
    code = "PTCM-E401"
    name = "AuthorizationException"
    
    def __init__(self, message: str = "권한이 없습니다"):
        super().__init__(message)

class RateLimitException(WCSException):
    code = "PTCM-E429"
    name = "RateLimitException"
    
    def __init__(self, message: str = "요청 한도를 초과했습니다"):
        super().__init__(message)

class UnknownException(WCSException):
    code = "PTCM-E999"
    name = "UnknownException"
    
    def __init__(self, message: str = "알 수 없는 오류가 발생했습니다"):
        super().__init__(message)