# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URL
from utility.logger import logger

# 스키마 생성 함수
def create_schema_if_not_exists():
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS user_service"))
            conn.commit()
        logger.info("user_service 스키마가 성공적으로 생성되었습니다.")
    except Exception as e:
        logger.error(f"user_service 스키마 생성 중 오류 발생: {e}")
        raise

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 스키마를 자동으로 생성하되 app.py에서도 명시적으로 호출할 수 있도록 함
create_schema_if_not_exists()

def get_db():
    
    try:
        db = SessionLocal() 
        yield db
    finally:
        db.close()
