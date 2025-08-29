from fastapi import APIRouter, Request
from .func.proxy_service_request import proxy_service_request

router = APIRouter()

@router.get("/health")
async def health_check():
    """Gateway health check endpoint"""
    return {"status": "healthy", "service": "gateway"}

@router.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_request(service_name: str, path: str, request: Request):
    """
    Generic proxy endpoint for all service requests
    """
    return await proxy_service_request(service_name, path, request)