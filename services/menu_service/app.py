# -*- coding: utf-8 -*-
import uuid

from fastapi import FastAPI, Request

from utility.db import Base, engine

from utility.logger import logger

# API router import
from api.v1.rest.menu_router import router as menu_router


def main():
    app = FastAPI(
        title="Menu Service API",
        description="Delivery App Menu Management Service",
        version="1.0.0"
    )
    
    # Register API router
    app.include_router(menu_router, prefix="/api/v1/rest")

    Base.metadata.create_all(bind=engine)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9110)


if __name__ == "__main__":
    main()