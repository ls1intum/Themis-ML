import logging
import sys

from fastapi import FastAPI, Response

from .notify import notify_themis_ml
from .random_feedback import get_random_feedbacks
from .test_submissions import get_test_submission_ids, get_test_submission

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()


@app.get("/")
def say_hello(response: Response):
    # "Artemis version"
    response.headers["Content-Version"] = "6.0.0"
    return "This route is needed for the auth check not to fail."


@app.get("/api/repository/{id}/files-content")
def get_repository(id: int):
    return get_test_submission(id)


@app.get("/api/programming-exercise-participations/{id}/latest-result-with-feedbacks")
def get_latest_result_with_feedbacks(id: int):
    return {
        "feedbacks": get_random_feedbacks(id)
    }


@app.get("/ids")
def get_ids():
    return get_test_submission_ids()


@app.get("/notify_for_all")
def notify_for_all():
    for id in get_test_submission_ids():
        notify_themis_ml(id)
    return "Done"
