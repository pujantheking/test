from fastapi import FastAPI
from core.utils import logger


def startup_events(_app: FastAPI) -> None:
    """
    Define startup events for the FastAPI application.
    """
    pass


def shutdown_events(_app: FastAPI):
    """
    Define shutdown events for the FastAPI application.
    """
    logger.info("Adding shutdown functions...")
