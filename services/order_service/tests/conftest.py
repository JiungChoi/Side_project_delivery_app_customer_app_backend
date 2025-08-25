"""
Pytest configuration and common fixtures for order service tests
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app
from utility.db import get_db
from model.order import Base

# Test database URL (SQLite in-memory for testing)
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop tables
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear overrides
    app.dependency_overrides.clear()


@pytest.fixture
def sample_restaurant_data():
    """Sample restaurant data for testing."""
    return {
        "id": "rest-001",
        "name": "테스트 레스토랑",
        "address": "서울시 강남구 테스트로 123",
        "phone": "02-1234-5678",
        "is_active": True
    }


@pytest.fixture
def sample_menu_data():
    """Sample menu data for testing."""
    return {
        "id": "menu-001",
        "restaurant_id": "rest-001",
        "name": "테스트 메뉴",
        "price": 15000,
        "description": "테스트 메뉴 설명",
        "is_available": True
    }


@pytest.fixture
def sample_address_data():
    """Sample address data for testing."""
    return {
        "id": "addr-001",
        "user_id": "user-123",
        "address": "서울시 강남구 배달주소 456",
        "detail_address": "101호",
        "postal_code": "12345",
        "is_default": True
    }


@pytest.fixture
def sample_create_order_request():
    """Sample create order request data."""
    return {
        "restaurant_id": "rest-001",
        "address_id": "addr-001",
        "payment_method": "card",
        "items": [
            {
                "menu_id": "menu-001",
                "quantity": 2,
                "special_requests": "매운맛으로 해주세요"
            }
        ],
        "delivery_instructions": "문 앞에 놓아주세요"
    } 