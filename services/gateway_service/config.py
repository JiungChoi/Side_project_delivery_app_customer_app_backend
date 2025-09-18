import os

class Config:
    # Server configuration
    HOST = "0.0.0.0"
    PORT = 9102
    
    # Service endpoints - using Docker internal hostnames
    SERVICE_ENDPOINTS = {
        "auth-service": "http://auth-service:9101/api/v1/rest",
        "user-service": "http://user-service:9111/api/v1/rest",
        "restaurant-service": "http://restaurant-service:9112/api/v1/rest",
        "menu-service": "http://menu-service:9110/api/v1/rest",
        "cart-service": "http://cart-service:9115/api/v1/rest",
        "order-service": "http://order-service:9109/api/v1/rest",
        "review-service": "http://review-service:9117/api/v1/rest",
        "customer-support-service": "http://customer-support-service:9105/api/v1/rest"
    }
    
    # Request timeout
    REQUEST_TIMEOUT = 30.0
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = ENVIRONMENT == "development"
    
    # Database (if needed for future features like rate limiting)
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres_main:5432/gateway_db")

    # Authentication configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7

    # Public endpoints that don't require authentication
    PUBLIC_ENDPOINTS = {
        "/api/v1/rest/health",
        "/api/v1/rest/auth-service/login",
        "/api/v1/rest/auth-service/signup",
        "/api/v1/rest/auth-service/refresh",
        "/api/v1/rest/restaurant-service/restaurants",  # Browse restaurants without login
        "/api/v1/rest/menu-service/restaurants",        # Browse menus without login
        "/api/v1/rest/user-service/exists",            # Check email/phone during signup
        # Cart service endpoints (temporary until login implemented)
        "/api/v1/rest/cart-service/cart",              # Cart operations
        "/api/v1/rest/cart-service/cart/items",        # Cart item operations
    }

    # Auth service internal URL for token verification
    AUTH_SERVICE_INTERNAL_URL = "http://auth-service:9101"