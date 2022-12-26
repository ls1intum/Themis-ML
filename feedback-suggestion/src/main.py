import sys
import logging
from fastapi import FastAPI, Request, Response, BackgroundTasks
from src import feedback_suggestion_ressource

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()
app.include_router(feedback_suggestion_ressource.router)
