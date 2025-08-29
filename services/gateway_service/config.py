import os

class Config:
    # Server configuration
    HOST = "0.0.0.0"
    PORT = 9102
    
    # Service endpoints - using Docker internal hostnames
    SERVICE_ENDPOINTS = {
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