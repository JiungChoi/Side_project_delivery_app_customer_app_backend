"""
Test cases for cancel order API
"""

import pytest
from fastapi import status
from sqlalchemy.orm import Session

from model.order import Order
from model.restaurant import Restaurant
from model.address import Address


class TestCancelOrder:
    """Test cases for PATCH /orders/{order_id}/cancel endpoint"""
    
    def test_cancel_order_success_pending(self, client, db_session):
        """Test successful order cancellation for pending order"""
        # Given: pending 상태의 주문이 존재
        order_id = self._setup_test_order(db_session, "pending")
        
        # When: 주문 취소 요청
        response = client.patch(f"/orders/{order_id}/cancel")
        
        # Then: 성공 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["order_id"] == order_id
        assert data["data"]["status"] == "cancelled"
    
    def test_cancel_order_success_paid(self, client, db_session):
        """Test successful order cancellation for paid order"""
        # Given: paid 상태의 주문이 존재
        order_id = self._setup_test_order(db_session, "paid")
        
        # When: 주문 취소 요청
        response = client.patch(f"/orders/{order_id}/cancel")
        
        # Then: 성공 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["order_id"] == order_id
        assert data["data"]["status"] == "cancelled"
    
    def test_cancel_order_not_found(self, client, db_session):
        """Test order cancellation with non-existent order ID"""
        # Given: 존재하지 않는 주문 ID
        order_id = "non-existent-order"
        
        # When: 주문 취소 요청
        response = client.patch(f"/orders/{order_id}/cancel")
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "OrderNotFoundException" in data["error"]["type"]
        assert f"주문 ID {order_id}를 찾을 수 없습니다" in data["error"]["message"]
    
    def test_cancel_order_invalid_status(self, client, db_session):
        """Test order cancellation with invalid status"""
        # Given: 취소할 수 없는 상태의 주문들
        invalid_statuses = ["preparing", "delivering", "completed", "cancelled"]
        
        for status in invalid_statuses:
            order_id = self._setup_test_order(db_session, status)
            
            # When: 주문 취소 요청
            response = client.patch(f"/orders/{order_id}/cancel")
            
            # Then: 실패 응답 확인
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is False
            assert "error" in data
            assert "OrderCancellationException" in data["error"]["type"]
            assert "취소할 수 없는 주문 상태입니다" in data["error"]["message"]
    
    def test_cancel_order_already_cancelled(self, client, db_session):
        """Test order cancellation for already cancelled order"""
        # Given: 이미 취소된 주문
        order_id = self._setup_test_order(db_session, "cancelled")
        
        # When: 주문 취소 요청
        response = client.patch(f"/orders/{order_id}/cancel")
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "OrderCancellationException" in data["error"]["type"]
    
    def test_cancel_order_completed(self, client, db_session):
        """Test order cancellation for completed order"""
        # Given: 완료된 주문
        order_id = self._setup_test_order(db_session, "completed")
        
        # When: 주문 취소 요청
        response = client.patch(f"/orders/{order_id}/cancel")
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "OrderCancellationException" in data["error"]["type"]
    
    def test_cancel_order_delivering(self, client, db_session):
        """Test order cancellation for delivering order"""
        # Given: 배달 중인 주문
        order_id = self._setup_test_order(db_session, "delivering")
        
        # When: 주문 취소 요청
        response = client.patch(f"/orders/{order_id}/cancel")
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "OrderCancellationException" in data["error"]["type"]
    
    def _setup_test_order(self, db_session: Session, order_status: str) -> str:
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
            id=f"order-{order_status}-001",
            user_id="user-123",
            restaurant_id="rest-001",
            address_id="addr-001",
            payment_method="card",
            status=order_status,
            total_amount=15000
        )
        db_session.add(order)
        db_session.commit()
        
        return order.id 