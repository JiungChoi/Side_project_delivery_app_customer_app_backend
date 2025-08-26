# -*- coding: utf-8 -*-
import uuid

from fastapi import FastAPI, Request

from utility.db import Base, engine

from utility.logger import logger

# API router import
from api.v1.rest.restaurant_router import router as restaurant_router


def main():
    app = FastAPI(
        title="Restaurant Service API",
        description="Restaurant Management Service",
        version="1.0.0"
    )
    
    # API router registration
    app.include_router(restaurant_router, prefix="/api/v1/rest")

    Base.metadata.create_all(bind=engine)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9112)


if __name__ == "__main__":
    main()