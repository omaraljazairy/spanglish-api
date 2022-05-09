import os
import logging
from pydantic import BaseSettings
from functools import lru_cache


logger = logging.getLogger('uvicorn')

class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 1)
    LOG_LEVEL = 'DEBUG' if environment == 'dev' else 'INFO'

    # logger.info(f"environment variables: {os.environ}")
    # logger.info(f"environment: {environment}")
    # logger.info(f"testing: {testing}")
    # logger.info(f"LOG_LEVEL: {LOG_LEVEL}")

@lru_cache()
def get_settings() -> BaseSettings:
    logger.info("Loading config settings from the environment.....")
    return Settings()