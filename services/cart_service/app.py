# -*- coding: utf-8 -*-
from fastapi import FastAPI

from utility.db import Base, engine
from utility.logger import logger

# API 라우터 import
from api.v1.rest.cart_router import router as cart_router


def main():
    app = FastAPI(
        title="Cart Service API",
        description="배달 앱 장바구니 관리 서비스",
        version="1.0.0"
    )
    
    # API 라우터 등록
    app.include_router(cart_router, prefix="/api/v1/rest")

    Base.metadata.create_all(bind=engine)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9115)


if __name__ == "__main__":
    main()