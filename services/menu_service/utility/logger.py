import logging
import sys
import colorlog

# 컬러로깅 핸들러 설정
handler = colorlog.StreamHandler(sys.stdout)
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s%(reset)s: %(message)s',
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
))

# 로거 설정
logger = logging.getLogger("menu_service")
logger.setLevel(logging.INFO)
logger.addHandler(handler)