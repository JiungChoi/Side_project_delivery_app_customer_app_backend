# -*- coding: utf-8 -*-
import uuid

from fastapi import FastAPI, Request

# 먼저 스키마를 생성하고 DB 설정
from utility.db import create_schema_if_not_exists, Base, engine

from utility.logger import logger

# API 라우터 import
from api.v1.rest.user_router import router as user_router


def main():
    # 스키마 먼저 생성 (명시적 호출)
    logger.info("사용자 서비스 스키마 생성을 시작합니다...")
    create_schema_if_not_exists()
    
    app = FastAPI(
        title="User Service API",
        description="배달 앱 사용자 관리 서비스",
        version="1.0.0"
    )
    
    # API 라우터 등록
    app.include_router(user_router, prefix="/api/v1/rest")

    # 테이블 생성
    logger.info("데이터베이스 테이블을 생성합니다...")
    Base.metadata.create_all(bind=engine)
    logger.info("user_service 시작 완료!")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9111)


if __name__ == "__main__":
    main()
