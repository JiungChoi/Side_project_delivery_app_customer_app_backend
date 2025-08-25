"""
Test cases for get my orders API
"""

import pytest
from fastapi import status
from sqlalchemy.orm import Session
from datetime import date, timedelta

from model.order import Order
from model.restaurant import Restaurant
from model.address import Address


class TestGetMyOrders:
    """Test cases for GET /orders/my endpoint"""
    
    def test_get_my_orders_success(self, client, db_session):
        """Test successful my orders retrieval"""
        # Given: 사용자의 주문 데이터가 DB에 존재
        self._setup_user_orders(db_session)
        
        # When: 내 주문 목록 조회 요청
        response = client.get("/orders/my")
        
        # Then: 성공 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]["orders"]) == 3  # 3개의 주문이 생성됨
    
    def test_get_my_orders_with_date_filter(self, client, db_session):
        """Test my orders retrieval with date filter"""
        # Given: 사용자의 주문 데이터가 DB에 존재
        self._setup_user_orders(db_session)
        
        # When: 날짜 필터와 함께 조회 요청
        today = date.today()
        response = client.get(f"/orders/my?start_date={today}&end_date={today}")
        
        # Then: 성공 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
    
    def test_get_my_orders_with_status_filter(self, client, db_session):
        """Test my orders retrieval with status filter"""
        # Given: 사용자의 주문 데이터가 DB에 존재
        self._setup_user_orders(db_session)
        
        # When: 상태 필터와 함께 조회 요청
        response = client.get("/orders/my?status=pending")
        
        # Then: 성공 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        # pending 상태의 주문만 반환되어야 함
        for order in data["data"]["orders"]:
            assert order["status"] == "pending"
    
    def test_get_my_orders_with_multiple_filters(self, client, db_session):
        """Test my orders retrieval with multiple filters"""
        # Given: 사용자의 주문 데이터가 DB에 존재
        self._setup_user_orders(db_session)
        
        # When: 여러 필터와 함께 조회 요청
        today = date.today()
        response = client.get(f"/orders/my?start_date={today}&status=completed")
        
        # Then: 성공 응답 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
    
    def test_get_my_orders_empty_result(self, client, db_session):
        """Test my orders retrieval with no matching orders"""
        # Given: 다른 사용자의 주문만 존재
        self._setup_other_user_orders(db_session)
        
        # When: 내 주문 목록 조회 요청
        response = client.get("/orders/my")
        
        # Then: 빈 결과 확인
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]["orders"]) == 0
    
    def test_get_my_orders_invalid_date_format(self, client, db_session):
        """Test my orders retrieval with invalid date format"""
        # Given: 잘못된 날짜 형식
        invalid_date = "2024-13-45"  # 잘못된 날짜
        
        # When: 잘못된 날짜로 조회 요청
        response = client.get(f"/orders/my?start_date={invalid_date}")
        
        # Then: 에러 응답 확인 (FastAPI가 자동으로 검증)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_my_orders_invalid_status(self, client, db_session):
        """Test my orders retrieval with invalid status"""
        # Given: 잘못된 상태값
        invalid_status = "invalid_status"
        
        # When: 잘못된 상태로 조회 요청
        response = client.get(f"/orders/my?status={invalid_status}")
        
        # Then: 성공 응답 확인 (비즈니스 로직에서 처리)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        # 잘못된 상태는 필터링되지 않고 모든 주문이 반환됨
        assert len(data["data"]["orders"]) == 0  # 필터링 결과 없음
    
    def _setup_user_orders(self, db_session: Session):
        """테스트용 사용자 주문들을 생성"""
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
            user_id="user-456",  # fixture에서 사용하는 user_id
            address="서울시 강남구 배달주소 456",
            detail_address="101호",
            postal_code="12345",
            is_default=True
        )
        db_session.add(address)
        
        # 다양한 상태의 주문들 생성
        statuses = ["pending", "completed", "cancelled"]
        for i, status in enumerate(statuses):
            order = Order(
                id=f"order-{i+1:03d}",
                user_id="user-456",  # fixture에서 사용하는 user_id
                restaurant_id="rest-001",
                address_id="addr-001",
                payment_method="card",
                status=status,
                total_amount=15000
            )
            db_session.add(order)
        
        db_session.commit()
    
    def _setup_other_user_orders(self, db_session: Session):
        """다른 사용자의 주문들을 생성"""
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
            user_id="other-user",
            address="서울시 강남구 배달주소 456",
            detail_address="101호",
            postal_code="12345",
            is_default=True
        )
        db_session.add(address)
        
        # 다른 사용자의 주문 생성
        order = Order(
            id="order-other-001",
            user_id="other-user",
            restaurant_id="rest-001",
            address_id="addr-001",
            payment_method="card",
            status="pending",
            total_amount=15000
        )
        db_session.add(order)
        
        db_session.commit() 