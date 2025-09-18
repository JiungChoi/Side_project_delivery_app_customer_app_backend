# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import json

print("[STARTUP] Starting cart service import process...")

try:
    from utility.db import Base, engine
    print("[STARTUP] Database utilities imported successfully")
except Exception as e:
    print(f"[STARTUP] Database import failed: {e}")

try:
    from utility.logger import logger
    print("[STARTUP] Logger imported successfully")
except Exception as e:
    print(f"[STARTUP] Logger import failed: {e}")

# API 라우터 import
try:
    from api.v1.rest.cart_router import router as cart_router
    print("[STARTUP] Cart router imported successfully")
except Exception as e:
    print(f"[STARTUP] Cart router import failed: {e}")


def main():
    print("[MAIN] Creating FastAPI application...")
    app = FastAPI(
        title="Cart Service API",
        description="배달 앱 장바구니 관리 서비스",
        version="1.0.0"
    )
    print("[MAIN] FastAPI application created successfully")

    # Middleware to log request bodies (fixed to avoid double body reading)
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        if request.method == "POST":
            print(f"[REQUEST_DEBUG] URL: {request.url}")
            print(f"[REQUEST_DEBUG] Method: {request.method}")
            print(f"[REQUEST_DEBUG] Headers: {dict(request.headers)}")

            # Create a new request with cached body
            body_bytes = await request.body()

            async def receive():
                return {"type": "http.request", "body": body_bytes}

            # Replace the receive callable
            request._receive = receive

            try:
                if body_bytes:
                    body_str = body_bytes.decode('utf-8')
                    print(f"[REQUEST_DEBUG] Raw Body: {body_str}")
                    try:
                        import json
                        parsed = json.loads(body_str)
                        print(f"[REQUEST_DEBUG] Parsed JSON: {parsed}")
                    except Exception as je:
                        print(f"[REQUEST_DEBUG] JSON Parse Error: {je}")
                else:
                    print(f"[REQUEST_DEBUG] Body: Empty")
            except Exception as e:
                print(f"[REQUEST_DEBUG] Failed to read body: {e}")

        response = await call_next(request)

        if request.method == "POST" and response.status_code >= 400:
            print(f"[REQUEST_DEBUG] Response Status: {response.status_code}")

        return response

    # Custom exception handler for validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        print(f"[VALIDATION_ERROR] ========== VALIDATION ERROR DETECTED ==========")
        print(f"[VALIDATION_ERROR] URL: {request.url}")
        print(f"[VALIDATION_ERROR] Method: {request.method}")
        print(f"[VALIDATION_ERROR] Headers: {dict(request.headers)}")
        print(f"[VALIDATION_ERROR] Query params: {dict(request.query_params)}")
        try:
            body = await request.body()
            body_str = body.decode('utf-8') if body else 'Empty'
            print(f"[VALIDATION_ERROR] Request body: {body_str}")
            if body_str and body_str != 'Empty':
                try:
                    import json
                    parsed_json = json.loads(body_str)
                    print(f"[VALIDATION_ERROR] Parsed JSON: {parsed_json}")
                except Exception as je:
                    print(f"[VALIDATION_ERROR] JSON parse error: {je}")
        except Exception as e:
            print(f"[VALIDATION_ERROR] Failed to read body: {e}")

        print(f"[VALIDATION_ERROR] Detailed validation errors:")
        for i, error in enumerate(exc.errors()):
            print(f"[VALIDATION_ERROR] Error {i+1}: {error}")
        print(f"[VALIDATION_ERROR] ================================================")
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "message": "Validation failed"}
        )

    # General exception handler
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        print(f"[GENERAL_ERROR] URL: {request.url}")
        print(f"[GENERAL_ERROR] Method: {request.method}")
        print(f"[GENERAL_ERROR] Exception: {exc}")
        import traceback
        print(f"[GENERAL_ERROR] Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    # 직접 엔드포인트 테스트
    @app.get("/test")
    async def direct_test():
        print("[APP] Direct test endpoint hit!")
        return {"status": "success", "message": "Direct endpoint works"}

    # API 라우터 등록
    app.include_router(cart_router, prefix="/api/v1/rest")

    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        print("[APP] Database tables created successfully")
    except Exception as e:
        print(f"[APP] Database initialization error (continuing anyway): {e}")

    print("[APP] FastAPI application setup completed successfully")
    print(f"[APP] Registered routes: {[route.path for route in app.routes]}")

    return app

# Create the FastAPI application instance
app = main()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9115)