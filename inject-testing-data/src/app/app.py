import logging
import sys

from fastapi import FastAPI, Response

from .notify import notify_themis_ml
from .generate_feedback import generate_feedback
from .test_submissions import get_test_submission, get_participation_ids

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


@app.get("/api/repository/{participation_id}/files-content")
def get_repository(participation_id: int):
    return get_test_submission(participation_id)


@app.get("/api/programming-exercise-participations/{participation_id}/latest-result-with-feedbacks")
def get_latest_result_with_feedbacks(participation_id: int):
    return {
        "feedbacks": generate_feedback(participation_id)
    }


@app.get("/ids/{exercise_id}")
def get_ids(exercise_id: int):
    return get_participation_ids(exercise_id)


@app.get("/notify_for_exercise/{exercise_id}")
def notify_for_all(exercise_id: int):
    for participation_id in get_participation_ids(exercise_id):
        notify_themis_ml(exercise_id, participation_id)
