import sys
import logging
from fastapi import FastAPI
from .endpoints import feedback_suggestion_request, feedback_suggestions

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()
app.include_router(feedback_suggestion_request.router)
app.include_router(feedback_suggestions.router)


@app.get("/")
def hello_world_message():
    logger.debug("-" * 80)
    logger.info("Hello World message requested!")

    return "Hello World, this is the Themis Feedback Suggestions Server!"