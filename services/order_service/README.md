# Order Service

배달 앱의 주문 관리를 담당하는 마이크로서비스입니다.

## 📋 목차

- [개요](#개요)
- [아키텍처](#아키텍처)
- [API 명세](#api-명세)
- [설치 및 실행](#설치-및-실행)
- [예외 처리](#예외-처리)
- [Result 패턴](#result-패턴)
- [개발 가이드](#개발-가이드)

## 🎯 개요

Order Service는 배달 앱에서 주문의 생성, 조회, 상태 관리, 취소 등의 기능을 제공하는 마이크로서비스입니다.

### 주요 기능

- 주문 생성 및 관리
- 주문 상태 추적
- 주문 취소 처리
- 주문 내역 조회
- 결제 연동

## 🏗️ 아키텍처

### 폴더 구조

```
order_service/
├── api/                    # API 엔드포인트
│   └── v1/
│       └── rest/
├── model/                  # 도메인 모델
│   ├── order.py           # 주문 엔티티
│   └── exception.py       # 예외 클래스들
├── repository/            # 데이터 접근 계층
├── schemas/               # DTO 및 스키마
│   ├── common.py         # 공통 스키마 (Result 패턴)
│   ├── request/          # 요청 DTO
│   └── response/         # 응답 DTO
├── utility/              # 유틸리티
│   ├── db.py            # 데이터베이스 설정
│   ├── logger.py        # 로깅 설정
│   └── enums.py         # 열거형
├── environments/         # 환경 설정
├── app.py               # FastAPI 애플리케이션
├── config.py            # 설정 관리
└── README.md            # 이 파일
```

### 클린 아키텍처 적용

- **Presentation Layer**: API 엔드포인트
- **Application Layer**: 비즈니스 로직
- **Domain Layer**: 도메인 모델 및 예외
- **Infrastructure Layer**: 데이터베이스, 외부 서비스

## 📡 API 명세

### A. 주문 생성 [POST] /orders

**설명**: 고객이 장바구니에서 결제를 누른 순간 호출

**요청**:

```json
{
  "restaurant_id": "uuid",
  "address_id": "uuid", 
  "payment_method": "card|cash|kakao|naver",
  "items": [
    {
      "menu_id": "uuid",
      "quantity": 2,
      "options": [
        {"menu_option_id": "uuid"}
      ]
    }
  ]
}
```

**응답**:

```json
{
  "data": {
    "order_id": "uuid",
    "status": "pending|paid",
    "total_price": 15000,
    "created_at": "2024-01-01T12:00:00"
  }
}
```

**응답 코드**:

- `201 Created`: 주문 생성 성공
- `400 Bad Request`: 잘못된 메뉴 ID 또는 옵션
- `401 Unauthorized`: 비로그인 상태
- `404 Not Found`: 매장 또는 메뉴 없음
- `409 Conflict`: 중복 주문 시도

### B. 주문 상세 조회 [GET] /orders/

**설명**: 주문완료 후 상세내역을 다시 확인할 때 호출

**응답**:

```json
{
  "data": {
    "order_id": "uuid",
    "user_id": "uuid",
    "address_id": "uuid",
    "total_price": 15000,
    "status": "pending",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00",
    "items": [
      {
        "menu_id": "uuid",
        "restaurant_id": "uuid",
        "quantity": 2,
        "price": 8000,
        "options": [
          {
            "menu_option_id": "uuid",
            "price": 1000
          }
        ]
      }
    ]
  }
}
```

### C. 내 주문 목록 조회 [GET] /orders/my

**설명**: 고객이 마이페이지 > 주문내역 보기를 클릭했을 때 호출

**쿼리 파라미터**:

- `start_date` (optional): 조회 시작 날짜
- `end_date` (optional): 조회 종료 날짜
- `status` (optional): 주문 상태 필터

**응답**:

```json
{
  "data": {
    "orders": [
      {
        "order_id": "uuid",
        "restaurant_id": "uuid",
        "status": "delivered",
        "total_price": 15000,
        "created_at": "2024-01-01T12:00:00"
      }
    ]
  }
}
```

### D. 주문 취소 [PATCH] /orders//cancel

**설명**: 고객이 결제된 주문을 취소할 때 호출 (pending, paid 상태일 때만)

**응답**:

```json
{
  "data": {
    "order_id": "uuid",
    "status": "cancelled",
    "cancelled_at": "2024-01-01T13:00:00"
  }
}
```

### E. 주문 상태 수동 업데이트 [PATCH] /orders

**설명**: 업주 앱에서 "조리시작" 버튼을 누르거나, 라이더가 "배달 시작"을 누를 때 호출

**요청**:

```json
{
  "order_id": "uuid",
  "new_status": "preparing|delivering"
}
```

**응답**:

```json
{
  "data": {
    "order_id": "uuid",
    "prev_status": "pending",
    "new_status": "preparing",
    "updated_at": "2024-01-01T13:00:00"
  }
}
```

### F. 주문 완료 처리 [POST] /orders//complete

**설명**: 라이더가 배달완료 버튼을 누를 때 호출

**응답**:

```json
{
  "data": {
    "order_id": "uuid",
    "status": "delivered",
    "completed_at": "2024-01-01T14:00:00"
  }
}
```

## 🚀 설치 및 실행

### 환경 요구사항

- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL

### 설치

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp environments/.env.example environments/.env.local
# .env.local 파일을 편집하여 데이터베이스 연결 정보 설정
```

### 실행

```bash
# 개발 모드 실행
python app.py

# 또는 uvicorn으로 실행
uvicorn app:app --host 0.0.0.0 --port 9109 --reload
```

### Docker 실행

```bash
docker-compose up -d
```

## ⚠️ 예외 처리

### 예외 클래스 계층 구조

```
WCSException (PTCM-E000)
├── ConnectionException (PTCM-E001)
├── OrderServiceException (PTCM-E100)
│   ├── OrderNotFoundException (PTCM-E101)
│   ├── OrderStatusException (PTCM-E102)
│   ├── OrderValidationException (PTCM-E103)
│   ├── PaymentException (PTCM-E104)
│   ├── OrderItemException (PTCM-E105)
│   ├── RestaurantNotFoundException (PTCM-E106)
│   ├── MenuNotFoundException (PTCM-E107)
│   ├── AddressNotFoundException (PTCM-E108)
│   ├── UserNotFoundException (PTCM-E109)
│   ├── OrderCancellationException (PTCM-E110)
│   └── OrderCompletionException (PTCM-E111)
├── DatabaseException (PTCM-E200)
├── ExternalServiceException (PTCM-E300)
├── AuthenticationException (PTCM-E400)
├── AuthorizationException (PTCM-E401)
├── RateLimitException (PTCM-E429)
└── UnknownException (PTCM-E999)
```

### 에러 코드 체계

- **PTCM-E000~E099**: WCS 기본 예외
- **PTCM-E100~E199**: 주문 서비스 예외
- **PTCM-E200~E299**: 데이터베이스 예외
- **PTCM-E300~E399**: 외부 서비스 예외
- **PTCM-E400~E499**: 인증/권한 예외
- **PTCM-E999**: 알 수 없는 예외

### 사용 예시

```python
from model.exception import OrderNotFoundException, PaymentException

def get_order(order_id: str):
    if not order_exists(order_id):
        raise OrderNotFoundException(f"주문 ID {order_id}를 찾을 수 없습니다")
  
    if payment_failed:
        raise PaymentException("결제에 실패했습니다")
```

## 🔄 Result 패턴

### 개요

Result 패턴은 함수의 반환값을 성공과 실패를 모두 포함하는 하나의 객체로 래핑하는 디자인 패턴입니다.

### 구조

```python
class ResultDto(BaseModel, Generic[T]):
    data: Optional[T] = None      # 성공 데이터
    error: Optional[ErrorDto] = None  # 에러 정보

class ErrorDto(BaseModel):
    code: str      # 에러 코드
    name: str      # 에러 이름
    message: str   # 에러 메시지
```

### 헬퍼 함수들

```python
# 성공 결과 생성
create_success_result(data)

# 에러 결과 생성
create_error_result(exception)

# 알 수 없는 에러 결과 생성
create_unknown_error_result(exception)
```

### 사용 예시

```python
from schemas.common import create_success_result, create_error_result
from model.exception import OrderNotFoundException
from schemas.response.create_order import CreateOrderResponseDto

def create_order_service(request):
    try:
        # 비즈니스 로직
        order = create_order(request)
        return CreateOrderResponseDto.create_result(order)
      
    except OrderNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)

# 결과 처리
result = create_order_service(request)
if result.error:
    print(f"에러: {result.error.code} - {result.error.message}")
else:
    print(f"성공: {result.data.order_id}")
```

### 장점

1. **일관된 응답 구조**: 성공/실패 모두 같은 형태
2. **예외 처리 개선**: 예외를 던지지 않고 결과 객체로 처리
3. **타입 안전성**: Generic을 통한 타입 보장
4. **에러 정보 풍부**: 에러 코드, 이름, 메시지 등 상세 정보

## 👨‍💻 개발 가이드

### 새로운 API 추가하기

1. **Request DTO 생성** (`schemas/request/`)

```python
class NewApiRequestDto(BaseModel):
    field1: str = Field(..., description="필드 설명")
    field2: int = Field(..., gt=0, description="양수만 허용")
```

2. **Response DTO 생성** (`schemas/response/`)

```python
class NewApiResponseDto(BaseModel):
    result: str = Field(..., description="결과")
  
    @classmethod
    def from_domain(cls, domain_object):
        return cls(result=domain_object.result)
  
    @classmethod
    def create_result(cls, domain_object):
        response_data = cls.from_domain(domain_object)
        return create_success_result(response_data)
```

3. **API 엔드포인트 추가** (`api/v1/rest/`)

```python
@router.post("/new-api")
async def new_api(request: NewApiRequestDto):
    try:
        result = new_api_service(request)
        return result
    except Exception as e:
        return create_unknown_error_result(e)
```

### 새로운 예외 추가하기

1. **예외 클래스 정의** (`model/exception.py`)

```python
class NewException(OrderServiceException):
    code = "PTCM-E112"
    name = "NewException"
  
    def __init__(self, message: str = "새로운 예외가 발생했습니다"):
        super().__init__(message)
```

2. **Result 패턴에 추가** (`schemas/common.py`)

```python
# import에 추가
from model.exception import NewException

# try_get_data_from_result 함수에 추가
elif code == "PTCM-E112":
    raise NewException(message)
```

### 테스트 작성하기

```python
import pytest
from schemas.request.create_order import CreateOrderRequestDto
from schemas.common import create_success_result

def test_create_order_success():
    request = CreateOrderRequestDto(
        restaurant_id="uuid",
        address_id="uuid",
        payment_method="card",
        items=[]
    )
  
    result = create_order_service(request)
    assert result.data is not None
    assert result.error is None

def test_create_order_validation_error():
    request = CreateOrderRequestDto(
        restaurant_id="invalid-uuid",
        address_id="uuid",
        payment_method="card",
        items=[]
    )
  
    result = create_order_service(request)
    assert result.data is None
    assert result.error.code == "PTCM-E103"
```

## 📝 변경 이력

### v1.0.0 (2024-01-01)

- 초기 버전 릴리즈
- 기본 CRUD API 구현
- Result 패턴 적용
- 예외 처리 체계 구축

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.
