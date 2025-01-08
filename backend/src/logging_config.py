import logging
import sys
import os
from datetime import datetime

# Create a custom formatter with timestamps and line numbers
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

LOG_DIR = "results/logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, f'model_loading_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Create file handler
file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)

# Configure logger
# logger = logging.getLogger('ModelLoader')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)