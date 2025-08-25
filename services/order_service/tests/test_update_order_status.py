"""
Test cases for update order status API
"""

import pytest
from fastapi import status
from sqlalchemy.orm import Session

from model.order import Order
from model.restaurant import Restaurant
from model.address import Address


class TestUpdateOrderStatus:
    """Test cases for PATCH /orders/ endpoint"""
    
    def test_update_order_status_success(self, client, db_session):
        """Test successful order status update"""
        # Given: pending 상태의 주문이 존재
        order_id = self._setup_test_order(db_session, "pending")
        
        # When: 주문 상태 업데이트 요청
        request_data = {
            "order_id": order_id,
            "new_status": "preparing"
        }
        response = client.patch("/orders/", json=request_data)
        
        # Then: 성공 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["order_id"] == order_id
        assert data["data"]["status"] == "preparing"
        assert data["data"]["previous_status"] == "pending"
    
    def test_update_order_status_valid_transitions(self, client, db_session):
        """Test order status update with valid status transitions"""
        # Given: 다양한 상태 전이 테스트
        valid_transitions = [
            ("pending", "preparing"),
            ("paid", "preparing"),
            ("preparing", "delivering"),
            ("delivering", "delivered")
        ]
        
        for current_status, new_status in valid_transitions:
            order_id = self._setup_test_order(db_session, current_status)
            
            # When: 주문 상태 업데이트 요청
            request_data = {
                "order_id": order_id,
                "new_status": new_status
            }
            response = client.patch("/orders/", json=request_data)
            
            # Then: 성공 응답 확인
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert data["data"]["status"] == new_status
            assert data["data"]["previous_status"] == current_status
    
    def test_update_order_status_not_found(self, client, db_session):
        """Test order status update with non-existent order ID"""
        # Given: 존재하지 않는 주문 ID
        request_data = {
            "order_id": "non-existent-order",
            "new_status": "preparing"
        }
        
        # When: 주문 상태 업데이트 요청
        response = client.patch("/orders/", json=request_data)
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "OrderNotFoundException" in data["error"]["type"]
    
    def test_update_order_status_invalid_transition(self, client, db_session):
        """Test order status update with invalid status transition"""
        # Given: 잘못된 상태 전이
        invalid_transitions = [
            ("pending", "delivering"),  # pending에서 바로 delivering으로 불가
            ("paid", "delivered"),      # paid에서 바로 delivered로 불가
            ("preparing", "pending"),   # preparing에서 pending으로 되돌아가기 불가
            ("delivering", "preparing") # delivering에서 preparing으로 되돌아가기 불가
        ]
        
        for current_status, new_status in invalid_transitions:
            order_id = self._setup_test_order(db_session, current_status)
            
            # When: 주문 상태 업데이트 요청
            request_data = {
                "order_id": order_id,
                "new_status": new_status
            }
            response = client.patch("/orders/", json=request_data)
            
            # Then: 실패 응답 확인
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is False
            assert "error" in data
            assert "OrderStatusException" in data["error"]["type"]
            assert f"{current_status}에서 {new_status}로 상태 변경이 불가능합니다" in data["error"]["message"]
    
    def test_update_order_status_final_states(self, client, db_session):
        """Test order status update for final states"""
        # Given: 최종 상태의 주문들
        final_states = ["delivered", "cancelled"]
        
        for final_state in final_states:
            order_id = self._setup_test_order(db_session, final_state)
            
            # When: 주문 상태 업데이트 요청
            request_data = {
                "order_id": order_id,
                "new_status": "preparing"
            }
            response = client.patch("/orders/", json=request_data)
            
            # Then: 실패 응답 확인
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is False
            assert "error" in data
            assert "OrderStatusException" in data["error"]["type"]
    
    def test_update_order_status_same_status(self, client, db_session):
        """Test order status update to the same status"""
        # Given: pending 상태의 주문
        order_id = self._setup_test_order(db_session, "pending")
        
        # When: 같은 상태로 업데이트 요청
        request_data = {
            "order_id": order_id,
            "new_status": "pending"
        }
        response = client.patch("/orders/", json=request_data)
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "OrderStatusException" in data["error"]["type"]
    
    def test_update_order_status_invalid_status_value(self, client, db_session):
        """Test order status update with invalid status value"""
        # Given: pending 상태의 주문
        order_id = self._setup_test_order(db_session, "pending")
        
        # When: 잘못된 상태값으로 업데이트 요청
        request_data = {
            "order_id": order_id,
            "new_status": "invalid_status"
        }
        response = client.patch("/orders/", json=request_data)
        
        # Then: 실패 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "OrderStatusException" in data["error"]["type"]
    
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