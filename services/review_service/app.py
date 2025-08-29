# -*- coding: utf-8 -*-
import uuid

from fastapi import FastAPI, Request

from utility.db import Base, engine

from utility.logger import logger

# API 라우터 import
from api.v1.rest.review_router import router as review_router


def main():
    app = FastAPI(
        title="Review Service API",
        description="배달 앱 리뷰 관리 서비스",
        version="1.0.0"
    )
    
    # API 라우터 등록
    app.include_router(review_router, prefix="/api/v1/rest")

    Base.metadata.create_all(bind=engine)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9117)


if __name__ == "__main__":
    main()