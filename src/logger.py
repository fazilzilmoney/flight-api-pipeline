import logging
import os

# create logs folder if not exists
if not os.path.exists('logs'):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()