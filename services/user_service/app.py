# -*- coding: utf-8 -*-
import uuid

from fastapi import FastAPI, Request

from utility.db import Base, engine

from utility.logger import logger

# API 라우터 import
from api.v1.rest.user_router import router as user_router


def main():
    app = FastAPI(
        title="User Service API",
        description="배달 앱 사용자 관리 서비스",
        version="1.0.0"
    )
    
    # API 라우터 등록
    app.include_router(user_router, prefix="/api/v1/rest")

    Base.metadata.create_all(bind=engine)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9111)


if __name__ == "__main__":
    main()
