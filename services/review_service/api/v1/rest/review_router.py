# -*- coding: utf-8 -*-
"""
Review API Router

리뷰 관련 API 엔드포인트들을 정의합니다.
"""

from fastapi import APIRouter, status
from uuid import UUID

# Request/Response DTOs
from schemas.request.create_review import CreateReviewRequestDto
from schemas.request.get_restaurant_reviews import GetRestaurantReviewsRequestDto
from schemas.request.get_my_reviews import GetMyReviewsRequestDto
from schemas.request.update_review import UpdateReviewRequestDto
from schemas.request.delete_review import DeleteReviewRequestDto

from schemas.response.create_review import CreateReviewResponseDto
from schemas.response.get_restaurant_reviews import GetRestaurantReviewsResponseDto
from schemas.response.get_my_reviews import GetMyReviewsResponseDto
from schemas.response.update_review import UpdateReviewResponseDto
from schemas.response.delete_review import DeleteReviewResponseDto

# Common schemas
from schemas.common import (
    ResultDto,
    create_success_result,
    create_error_result,
    create_unknown_error_result
)

# Exception classes
from model.exception import (
    ReviewNotFoundException,
    ReviewValidationException,
    ReviewPermissionException,
    OrderNotFoundException,
    OrderNotCompletedException,
    ReviewAlreadyExistsException,
    RestaurantNotFoundException,
    UserNotFoundException,
    AuthenticationException,
    AuthorizationException
)

# Business logic functions
from .func.try_create_review import try_create_review
from .func.try_get_restaurant_reviews import try_get_restaurant_reviews
from .func.try_get_my_reviews import try_get_my_reviews
from .func.try_update_review import try_update_review
from .func.try_delete_review import try_delete_review

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("", response_model=ResultDto, status_code=status.HTTP_201_CREATED)
async def create_review(request: CreateReviewRequestDto):
    """
    리뷰 작성 API
    
    고객이 배달 완료된 주문에 대해 리뷰를 작성하고 등록 버튼을 눌렀을 때 호출됩니다.
    """
    try:
        result = await try_create_review(request)
        return result
    except ReviewValidationException as e:
        return create_error_result(e)
    except OrderNotFoundException as e:
        return create_error_result(e)
    except OrderNotCompletedException as e:
        return create_error_result(e)
    except ReviewAlreadyExistsException as e:
        return create_error_result(e)
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.get("/restaurants/{restaurant_id}/reviews", response_model=ResultDto)
async def get_restaurant_reviews(
    restaurant_id: UUID,
    page: int = 1,
    limit: int = 10,
    rating_filter: int = None
):
    """
    특정 매장의 리뷰 목록 조회 API
    
    고객이 매장 상세 페이지의 리뷰 탭을 열었을 때 호출됩니다.
    """
    try:
        request = GetRestaurantReviewsRequestDto(
            page=page,
            limit=limit,
            rating_filter=rating_filter
        )
        result = await try_get_restaurant_reviews(restaurant_id, request)
        return result
    except RestaurantNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.get("/my", response_model=ResultDto)
async def get_my_reviews(user_id: UUID, page: int = 1, limit: int = 10):
    """
    내가 작성한 리뷰 목록 조회 API
    
    마이페이지 > 나의 리뷰 목록 보기 클릭 시 호출됩니다.
    """
    try:
        request = GetMyReviewsRequestDto(
            user_id=user_id,
            page=page,
            limit=limit
        )
        result = await try_get_my_reviews(request)
        return result
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.patch("/{review_id}", response_model=ResultDto)
async def update_review(review_id: UUID, request: UpdateReviewRequestDto):
    """
    리뷰 수정 API
    
    고객이 본인이 작성한 리뷰를 수정하고 저장했을 때 호출됩니다.
    """
    try:
        result = await try_update_review(review_id, request)
        return result
    except ReviewNotFoundException as e:
        return create_error_result(e)
    except ReviewPermissionException as e:
        return create_error_result(e)
    except ReviewValidationException as e:
        return create_error_result(e)
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.delete("/{review_id}", response_model=ResultDto)
async def delete_review(review_id: UUID, user_id: UUID):
    """
    리뷰 삭제 API
    
    고객이 본인의 리뷰를 삭제했을 때 호출됩니다.
    """
    try:
        request = DeleteReviewRequestDto(user_id=user_id)
        result = await try_delete_review(review_id, request)
        return result
    except ReviewNotFoundException as e:
        return create_error_result(e)
    except ReviewPermissionException as e:
        return create_error_result(e)
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)