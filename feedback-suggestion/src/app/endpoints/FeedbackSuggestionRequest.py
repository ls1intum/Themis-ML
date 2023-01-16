from logging import getLogger
from fastapi import APIRouter, HTTPException
from ..database.FeedbackSuggestionEntity import FeedbackSuggestionEntity
from .authenticated_request import AuthRequest
from pydantic import BaseModel
from ..extract_methods.extract_methods import extract_methods
from .feedback import Feedback
from typing import List
from ..extract_methods.method_node import MethodNode

logger = getLogger(name="FeedbackSuggestionRequest")
router = APIRouter()
db = FeedbackSuggestionEntity()


@router.get("/feedback_suggestion/insert")
def insert_name():
    logger.debug("-" * 80)
    logger.info("Insert message requested!")

    __fs = FeedbackSuggestionEntity()
    __fs.insert_name(
        first_name="firstname", last_name="lastname", email="firstname@lastname.de"
    )

    return "Name inserted!"


@router.get("/feedback_suggestion/fetch")
def fetch_name():
    logger.debug("-" * 80)
    logger.info("Fetch message requested!")

    __fs = FeedbackSuggestionEntity()
    response = __fs.fetch_name()

    return response


class NotifyRequest(BaseModel):
    token: str
    exercise_id: int
    participation_id: int
    server: str


@router.post("/feedback_suggestion/notify")
def load_feedbacks(request: NotifyRequest):
    logger.debug("-" * 80)
    logger.info("Notified about new feedback!")

    auth_request = AuthRequest(request.token, request.server)
    response = auth_request.get(f"/repository/{request.participation_id}/files-content")
    files: dict = { name: content for name, content in response.json().items() if name.endswith(".java") }

    response = auth_request.get(f"/programming-exercise-participations/{request.participation_id}/latest-result-with-feedbacks")
    res_json = response.json()
    if "feedbacks" not in res_json:
        raise HTTPException(status_code=400, detail="No feedbacks for assessment found. Assessment might not be submitted.")
    feedbacks = [ReceivedFeedback(f["text"], f["detailText"], f["credits"]) for f in res_json["feedbacks"] if f["type"] == "MANUAL"]

    method_feedbacks = []
    for filepath, content in files.items():
        methods: List[MethodNode] = extract_methods(content)
        for method in methods:
            start = method.get_start_line()
            stop = method.get_stop_line()
            for feedback in feedbacks:
                if feedback.file == "/" + filepath and feedback.from_line >= start and feedback.to_line <= stop:
                    method_feedbacks.append(
                        Feedback(
                            exercise_id=request.exercise_id,
                            participation_id=request.participation_id,
                            code=method.get_source_code(),
                            src_file=filepath,
                            from_line=feedback.from_line,
                            to_line=feedback.to_line,
                            text=feedback.detailText,
                            credits=feedback.credits
                        )
                    )
    db.store_feedbacks(method_feedbacks)

    return "Success!"

class ReceivedFeedback():
    def __init__(self, text, detailText, credits):
        self.text = text
        self.detailText = detailText
        self.credits = credits
        self.file = self.parse_filename()
        self.from_line, self.to_line = self.parse_lines()

    def parse_filename(self):
        return self.text.split()[1]

    def parse_lines(self):
        if "at lines" in self.text:
            lines = self.text.split()[-1]
            line_nums = lines.split("-")
            return int(line_nums[0]), int(line_nums[1])
        else:
            line_num = int(self.text.split()[-3])
            return line_num, line_num



@router.get("/feedback_suggestions/feedbacks")
def get_feedbacks():
    return db.fetch_feedbacks()
