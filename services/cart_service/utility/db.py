from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 스키마 생성
try:
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS cart_service"))
        # Best-effort schema migration for cart_item_option
        try:
            conn.execute(text("""
                ALTER TABLE cart_service.cart_item_option 
                ADD COLUMN IF NOT EXISTS menu_option_name VARCHAR;
            """))
            conn.execute(text("""
                ALTER TABLE cart_service.cart_item_option 
                ALTER COLUMN menu_option_id DROP NOT NULL;
            """))
            conn.commit()
        except Exception as _:
            # ignore migration issues to avoid startup failure
            pass
        conn.commit()
except Exception as e:
    print(f"Schema creation warning: {e}")

def get_db():
    
    try:
        db = SessionLocal() 
        yield db
    finally:
        db.close()
