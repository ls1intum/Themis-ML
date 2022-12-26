import json
from logging import getLogger
from fastapi import APIRouter, Request

logger = getLogger(name="FeedSuggestionRessource")
router = APIRouter()

@router.get("/")
def helloWorldMessage():
    logger.debug("-" * 80)
    logger.info("Hello World message requested!")

    return "Hello World, this is the Themis Feedback Suggestions Server!"
