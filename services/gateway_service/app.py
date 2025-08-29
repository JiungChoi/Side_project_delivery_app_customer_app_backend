# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Config
from utility.logger import logger

# API router import
from api.v1.rest.gateway_router import router as gateway_router

def main():
    app = FastAPI(
        title="Gateway Service API",
        description="API Gateway for microservices",
        version="1.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # API router registration
    app.include_router(gateway_router, prefix="/api/v1/rest")
    
    logger.info("Gateway service initialized successfully")
    
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)

if __name__ == "__main__":
    main()