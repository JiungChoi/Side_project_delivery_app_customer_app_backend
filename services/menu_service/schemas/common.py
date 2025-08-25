from pydantic import BaseModel
from typing import Any, Optional

class ResultDto(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[Any] = None


def create_success_result(data: Any) -> ResultDto:
    return ResultDto(success=True, data=data)

def create_error_result(error: Exception) -> ResultDto:
    return ResultDto(success=False, error={
        "type": error.__class__.__name__,
        "message": str(error)
    })

def create_unknown_error_result(error: Exception) -> ResultDto:
    return ResultDto(success=False, error={
        "type": "UnknownException",
        "message": str(error)
    }) 