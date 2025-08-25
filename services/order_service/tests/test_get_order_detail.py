"""
Test cases for get order detail API
"""

import pytest
from fastapi import status
from sqlalchemy.orm import Session

from model.order import Order
from model.restaurant import Restaurant
from model.menu import Menu
from model.address import Address


class TestGetOrderDetail:
    """Test cases for GET /orders/{order_id} endpoint"""
    
    def test_get_order_detail_success(self, client, db_session):
        """Test successful order detail retrieval"""
        # Given: 주문 데이터가 DB에 존재
        order_id = self._setup_test_order(db_session)
        
        # When: 주문 상세 조회 요청
        response = client.get(f"/orders/{order_id}")
        
        # Then: 성공 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["order_id"] == order_id
        assert data["data"]["status"] == "pending"
        assert data["data"]["restaurant_id"] == "rest-001"
        assert data["data"]["address_id"] == "addr-001"
    
    def test_get_order_detail_not_found(self, client, db_session):
        """Test order detail retrieval with non-existent order ID"""
        # Given: 존재하지 않는 주문 ID
        order_id = "non-existent-order"
        
        # When: 주문 상세 조회 요청
        response = client.get(f"/orders/{order_id}")
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "OrderNotFoundException" in data["error"]["type"]
        assert f"주문 ID {order_id}를 찾을 수 없습니다" in data["error"]["message"]
    
    def test_get_order_detail_invalid_id_format(self, client, db_session):
        """Test order detail retrieval with invalid ID format"""
        # Given: 잘못된 형식의 주문 ID
        order_id = "invalid-format-123"
        
        # When: 주문 상세 조회 요청
        response = client.get(f"/orders/{order_id}")
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "OrderNotFoundException" in data["error"]["type"]
    
    def test_get_order_detail_with_different_statuses(self, client, db_session):
        """Test order detail retrieval for orders with different statuses"""
        # Given: 다양한 상태의 주문들 생성
        order_ids = self._setup_orders_with_different_statuses(db_session)
        
        for order_id in order_ids:
            # When: 주문 상세 조회 요청
            response = client.get(f"/orders/{order_id}")
            
            # Then: 성공 응답 확인
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert "data" in data
            assert data["data"]["order_id"] == order_id
    
    def _setup_test_order(self, db_session: Session) -> str:
        """테스트용 주문을 생성하고 ID를 반환"""
        # 기본 데이터 생성
        restaurant = Restaurant(
            id="rest-001",
            name="테스트 레스토랑",
            address="서울시 강남구 테스트로 123",
            phone="02-1234-5678",
            is_active=True
        )
        db_session.add(restaurant)
        
        menu = Menu(
            id="menu-001",
            restaurant_id="rest-001",
            name="테스트 메뉴",
            price=15000,
            description="테스트 메뉴 설명",
            is_available=True
        )
        db_session.add(menu)
        
        address = Address(
            id="addr-001",
            user_id="user-123",
            address="서울시 강남구 배달주소 456",
            detail_address="101호",
            postal_code="12345",
            is_default=True
        )
        db_session.add(address)
        
        # 주문 생성
        order = Order(
            id="order-001",
            user_id="user-123",
            restaurant_id="rest-001",
            address_id="addr-001",
            payment_method="card",
            status="pending",
            total_amount=15000
        )
        db_session.add(order)
        db_session.commit()
        
        return order.id
    
    def _setup_orders_with_different_statuses(self, db_session: Session) -> list:
        """다양한 상태의 주문들을 생성하고 ID 리스트를 반환"""
        # 기본 데이터 생성
        restaurant = Restaurant(
            id="rest-001",
            name="테스트 레스토랑",
            address="서울시 강남구 테스트로 123",
            phone="02-1234-5678",
            is_active=True
        )
        db_session.add(restaurant)
        
        address = Address(
            id="addr-001",
            user_id="user-123",
            address="서울시 강남구 배달주소 456",
            detail_address="101호",
            postal_code="12345",
            is_default=True
        )
        db_session.add(address)
        
        # 다양한 상태의 주문들 생성
        statuses = ["pending", "paid", "preparing", "delivering", "completed", "cancelled"]
        order_ids = []
        
        for i, status in enumerate(statuses):
            order = Order(
                id=f"order-{i+1:03d}",
                user_id="user-123",
                restaurant_id="rest-001",
                address_id="addr-001",
                payment_method="card",
                status=status,
                total_amount=15000
            )
            db_session.add(order)
            order_ids.append(order.id)
        
        db_session.commit()
        return order_ids 