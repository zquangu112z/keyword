import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler()
stdout_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(stdout_format)
logger.addHandler(stdout_handler)

WEBSITES_DATA_FILEPATH = os.environ.get(
    "WEBSITES_DATA_FILEPATH",
    "./data/check_list.csv"
)

KEY_WORDS = ["America", "Europe", "Asia", "Africa", "Australia"]

CHROMEDRIVER_PATH = os.environ.get(
    "CHROMEDRIVER_PATH",
    "driver/chromedriver"
)
