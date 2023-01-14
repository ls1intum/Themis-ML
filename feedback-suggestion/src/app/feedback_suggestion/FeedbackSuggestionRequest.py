from logging import getLogger
from fastapi import APIRouter
from ..database.FeedbackSuggestionEntity import FeedbackSuggestionEntity

logger = getLogger(name="FeedbackSuggestionRequest")
router = APIRouter()


@router.get("/feedback_suggestion/insert")
def insert_name():
    logger.debug("-" * 80)
    logger.info("Insert message requested!")

    __fs = FeedbackSuggestionEntity()
    __fs.insert_name(first_name="firstname", last_name="lastname", email="firstname@lastname.de")

    return "Name inserted!"


@router.get("/feedback_suggestion/fetch")
def fetch_name():
    logger.debug("-" * 80)
    logger.info("Fetch message requested!")

    __fs = FeedbackSuggestionEntity()
    response = __fs.fetch_name()

    return response
