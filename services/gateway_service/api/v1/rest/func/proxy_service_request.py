import httpx
from fastapi import HTTPException, Request
from config import Config
from utility.logger import logger

async def proxy_service_request(service_name: str, path: str, request: Request):
    """
    Proxy requests to backend services
    """
    if service_name not in Config.SERVICE_ENDPOINTS:
        logger.error(f"Unknown service: {service_name}")
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    service_url = Config.SERVICE_ENDPOINTS[service_name]
    # Build target URL without forcing trailing slash
    if path:
        target_url = f"{service_url}/{path}"
    else:
        target_url = service_url
    
    # Get request details
    method = request.method
    headers = dict(request.headers)
    
    # Remove host header to avoid conflicts
    headers.pop("host", None)
    
    logger.info(f"Proxying {method} request to {target_url}")
    
    try:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(
                    target_url,
                    headers=headers,
                    params=request.query_params,
                    timeout=Config.REQUEST_TIMEOUT
                )
            else:
                body = await request.body()
                response = await client.request(
                    method,
                    target_url,
                    headers=headers,
                    content=body,
                    params=request.query_params,
                    timeout=Config.REQUEST_TIMEOUT
                )
            
            logger.info(f"Service response status: {response.status_code}")
            
            # Return JSON if content type is JSON, otherwise return text
            if response.headers.get("content-type", "").startswith("application/json"):
                return response.json()
            else:
                return response.text
                
    except httpx.RequestError as e:
        logger.error(f"Request error: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP status error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal gateway error")