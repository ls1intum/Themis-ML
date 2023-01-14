import sys
import logging
from fastapi import FastAPI
from .app.feedback_suggestion import FeedbackSuggestionRequest

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()
app.include_router(FeedbackSuggestionRequest.router)


@app.get("/")
def hello_world_message():
    logger.debug("-" * 80)
    logger.info("Hello World message requested!")

    return "Hello World, this is the Themis Feedback Suggestions Server!"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)