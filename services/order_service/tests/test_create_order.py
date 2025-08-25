"""
Test cases for create order API
"""

import pytest
from fastapi import status
from sqlalchemy.orm import Session

from model.restaurant import Restaurant
from model.menu import Menu
from model.address import Address


class TestCreateOrder:
    """Test cases for POST /orders/ endpoint"""
    
    def test_create_order_success(self, client, db_session, sample_create_order_request):
        """Test successful order creation"""
        # Given: 필요한 데이터가 DB에 존재
        self._setup_test_data(db_session)
        
        # When: 주문 생성 요청
        response = client.post("/orders/", json=sample_create_order_request)
        
        # Then: 성공 응답 확인
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["order_id"] is not None
        assert data["data"]["status"] == "pending"
        assert data["data"]["restaurant_id"] == sample_create_order_request["restaurant_id"]
        assert data["data"]["address_id"] == sample_create_order_request["address_id"]
    
    def test_create_order_without_items(self, client, db_session):
        """Test order creation without items (should fail)"""
        # Given: 빈 아이템 리스트로 요청
        request_data = {
            "restaurant_id": "rest-001",
            "address_id": "addr-001",
            "payment_method": "card",
            "items": [],
            "delivery_instructions": "문 앞에 놓아주세요"
        }
        
        # When: 주문 생성 요청
        response = client.post("/orders/", json=request_data)
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK  # Result 패턴 사용
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "주문 아이템이 없습니다" in data["error"]["message"]
    
    def test_create_order_invalid_restaurant(self, client, db_session, sample_create_order_request):
        """Test order creation with invalid restaurant ID"""
        # Given: 존재하지 않는 레스토랑 ID
        request_data = sample_create_order_request.copy()
        request_data["restaurant_id"] = "invalid-restaurant"
        
        # When: 주문 생성 요청
        response = client.post("/orders/", json=request_data)
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "RestaurantNotFoundException" in data["error"]["type"]
    
    def test_create_order_invalid_address(self, client, db_session, sample_create_order_request):
        """Test order creation with invalid address ID"""
        # Given: 존재하지 않는 주소 ID
        request_data = sample_create_order_request.copy()
        request_data["address_id"] = "invalid-address"
        
        # When: 주문 생성 요청
        response = client.post("/orders/", json=request_data)
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "AddressNotFoundException" in data["error"]["type"]
    
    def test_create_order_invalid_menu(self, client, db_session, sample_create_order_request):
        """Test order creation with invalid menu ID"""
        # Given: 존재하지 않는 메뉴 ID
        request_data = sample_create_order_request.copy()
        request_data["items"][0]["menu_id"] = "invalid-menu"
        
        # When: 주문 생성 요청
        response = client.post("/orders/", json=request_data)
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "MenuNotFoundException" in data["error"]["type"]
    
    def test_create_order_multiple_items(self, client, db_session):
        """Test order creation with multiple items"""
        # Given: 여러 아이템이 있는 주문 요청
        self._setup_test_data(db_session)
        
        # 추가 메뉴 생성
        menu2 = Menu(
            id="menu-002",
            restaurant_id="rest-001",
            name="테스트 메뉴 2",
            price=20000,
            description="테스트 메뉴 2 설명",
            is_available=True
        )
        db_session.add(menu2)
        db_session.commit()
        
        request_data = {
            "restaurant_id": "rest-001",
            "address_id": "addr-001",
            "payment_method": "card",
            "items": [
                {
                    "menu_id": "menu-001",
                    "quantity": 2,
                    "special_requests": "매운맛으로 해주세요"
                },
                {
                    "menu_id": "menu-002",
                    "quantity": 1,
                    "special_requests": "덜 매운맛으로 해주세요"
                }
            ],
            "delivery_instructions": "문 앞에 놓아주세요"
        }
        
        # When: 주문 생성 요청
        response = client.post("/orders/", json=request_data)
        
        # Then: 성공 응답 확인
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["order_id"] is not None
    
    def test_create_order_different_payment_methods(self, client, db_session, sample_create_order_request):
        """Test order creation with different payment methods"""
        # Given: 필요한 데이터가 DB에 존재
        self._setup_test_data(db_session)
        
        payment_methods = ["card", "cash", "mobile"]
        
        for payment_method in payment_methods:
            # Given: 다른 결제 방법으로 요청
            request_data = sample_create_order_request.copy()
            request_data["payment_method"] = payment_method
            
            # When: 주문 생성 요청
            response = client.post("/orders/", json=request_data)
            
            # Then: 성공 응답 확인
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["success"] is True
            assert data["data"]["payment_method"] == payment_method
    
    def _setup_test_data(self, db_session: Session):
        """테스트에 필요한 기본 데이터를 DB에 설정"""
        # 레스토랑 생성
        restaurant = Restaurant(
            id="rest-001",
            name="테스트 레스토랑",
            address="서울시 강남구 테스트로 123",
            phone="02-1234-5678",
            is_active=True
        )
        db_session.add(restaurant)
        
        # 메뉴 생성
        menu = Menu(
            id="menu-001",
            restaurant_id="rest-001",
            name="테스트 메뉴",
            price=15000,
            description="테스트 메뉴 설명",
            is_available=True
        )
        db_session.add(menu)
        
        # 주소 생성
        address = Address(
            id="addr-001",
            user_id="user-123",
            address="서울시 강남구 배달주소 456",
            detail_address="101호",
            postal_code="12345",
            is_default=True
        )
        db_session.add(address)
        
        db_session.commit() 