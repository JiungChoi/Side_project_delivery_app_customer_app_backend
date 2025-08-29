import logging
import sys
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO if Config.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("gateway_service")