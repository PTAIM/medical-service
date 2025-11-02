import logging

logging.basicConfig(level=logging.INFO)
app_logger = logging.getLogger("APP_LOGGER")
app_logger.info("Logger initialized for the application.")
