# Backend Microservices Requirements for Delivery App

## 서비스 및 포트 정보

| 서비스명                  | 포트 | 역할 요약                         |
| ------------------------- | ---- | --------------------------------- |
| auth_service              | 9101 | 인증, 인가, 세션 관리             |
| gateway_service           | 9102 | API 통합 진입점, 인증/라우팅/로깅 |
| system_alert_service      | 9103 | 시스템 이벤트/에러/경고 알림      |
| delivery_tracking_service | 9104 | 배송 위치 실시간 추적             |
| customer_support_service  | 9105 | 고객 문의/FAQ/실시간 채팅         |
| notification_service      | 9106 | 푸시알림, SMS, 앱 내 알림         |
| review_service            | 9107 | 리뷰/평점/사진 첨부               |
| payment_service           | 9108 | 결제수단, 결제 처리, 포인트/쿠폰  |
| order_service             | 9109 | 주문 생성/조회/상태변경/취소      |
| cart_service              | 9110 | 장바구니 생성/조회/수정/삭제      |
| menu_service              | 9111 | 메뉴/옵션/이미지 관리             |
| restaurant_service        | 9112 | 음식점 정보/검색/상세/메뉴 제공   |
| user_service              | 9113 | 회원가입/로그인/프로필/정보관리   |

---

## Common

- 모든 서비스는 FastAPI 기반 REST API로 구현
- 데이터베이스는 PostgreSQL, ORM 사용 (예: SQLAlchemy)
- 각 서비스는 Docker 컨테이너로 배포
- 서비스 간 통신은 REST 또는 메시지 브로커(추후 확장)
- 인증/인가는 JWT 기반(추후 OAuth2 등 확장 가능)

---

## 1. User Service

- 회원가입 (이메일/비밀번호, 소셜 로그인)
- 로그인/로그아웃, JWT 발급
- 사용자 프로필 관리 (이름, 전화번호, 주소 복수 관리)
- 개인정보 수정, 알림 설정
- 사용자 정보 조회/수정/삭제

## 2. Restaurant Service

- 음식점 등록/수정/삭제 (관리자용)
- 음식점 기본 정보 제공 (영업시간, 배달팁, 최소주문금액 등)
- 위치 기반 음식점 검색 (좌표/주소 기반)
- 카테고리/태그/이름/메뉴 검색
- 음식점 상세 정보 및 메뉴/옵션 제공

## 3. Menu Service

- 메뉴/옵션 그룹/옵션 CRUD (음식점별)
- 메뉴 상세 정보 제공
- 메뉴 이미지 관리 (이미지 업로드/조회)

## 4. Cart Service

- 장바구니 생성/조회/수정/삭제 (사용자별)
- 메뉴/옵션 추가, 수량 조절
- 최소주문금액, 배달팁 계산

## 5. Order Service

- 주문 생성/조회/상태변경/취소/환불
- 주문 상태 추적 (주문~배달완료)
- 주문 내역 조회, 재주문
- 결제 연동(외부 결제 서비스와 연동)

## 6. Payment Service

- 결제수단 등록/삭제/조회 (카드, 간편결제 등)
- 결제 처리, 결제 내역 관리
- 포인트/쿠폰 사용 및 관리

## 7. Review Service

- 리뷰 작성/수정/삭제 (주문 완료 후)
- 음식점별 리뷰 목록/평점 통계/필터링
- 리뷰 사진 첨부
- 사용자 작성 리뷰 관리

## 8. Notification Service

- 주문 상태 변경/프로모션/리뷰 요청 알림
- 푸시/앱 내 알림 발송
- 알림 설정 관리

## 9. Customer Support Service

- FAQ, 1:1 문의, 주문 관련 문의
- 실시간 채팅/전화 연결(외부 연동)

## 10. Delivery Tracking Service

- 배송 위치 실시간 추적 및 상태 관리

## 11. Auth Service

- 인증, 인가, 세션 관리(JWT 등)

## 12. System Alert Service

- 시스템 이벤트, 에러, 경고 알림 관리

## 13. Gateway Service

- API 통합 진입점, 인증/라우팅/로깅/Rate Limiting

---

## 공통 기술 스택

- Python 3.11+, FastAPI, SQLAlchemy, Alembic
- PostgreSQL
- Docker, Docker Compose
- pytest, httpx 등 테스트 도구
- Swagger(OpenAPI) 문서 자동화

---

## 서비스별 디렉토리 예시

- auth_service/
- gateway_service/
- system_alert_service/
- delivery_tracking_service/
- customer_support_service/
- notification_service/
- review_service/
- payment_service/
- order_service/
- cart_service/
- menu_service/
- restaurant_service/
- user_service/

각 서비스별로 main.py, models.py, schemas.py, crud.py, api/, tests/ 등 표준 구조로 작성
