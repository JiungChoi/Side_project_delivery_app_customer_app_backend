# -*- coding: utf-8 -*-
import logging
import sys

# UTF-8 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')

# 로거 생성
logger = logging.getLogger("customer_support_service")
logger.setLevel(logging.INFO)

# 핸들러가 이미 추가되어 있는지 확인
if not logger.handlers:
    # 콘솔 핸들러 생성
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # 포맷터 생성
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # 핸들러를 로거에 추가
    logger.addHandler(console_handler)