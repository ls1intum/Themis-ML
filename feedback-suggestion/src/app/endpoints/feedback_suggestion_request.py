from logging import getLogger
from typing import List, Union

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

from .auth_token import get_auth_token
from .authenticated_request import AuthRequest
from ..database.feedback_suggestion_entity import FeedbackSuggestionEntity
from ..extract_methods.extract_methods import extract_methods
from ..extract_methods.method_node import MethodNode
from ..feedback_suggestion.feedback import Feedback

logger = getLogger(name="FeedbackSuggestionRequest")
router = APIRouter()
db = FeedbackSuggestionEntity()


class NotifyRequest(BaseModel):
    exercise_id: int
    participation_id: int
    server: str


@router.post("/feedback_suggestion/notify")
def load_feedbacks(
    request: NotifyRequest,
    authorization: Union[str, None] = Header()
):
    logger.debug("-" * 80)
    logger.info("Notified about new feedback!")

    token = get_auth_token(authorization)

    auth_request = AuthRequest(token, request.server)
    # Make sure to not reveal sensitive information before this request!
    response = auth_request.get(f"/repository/{request.participation_id}/files-content")
    if not response.ok:
        print("Error with status code", response.status_code)
        raise HTTPException(status_code=response.status_code, detail="Error on Artemis server: " + response.text)
    files: dict = {name: content for name, content in response.json().items() if name.endswith(".java")}

    response = auth_request.get(
        f"/programming-exercise-participations/{request.participation_id}/latest-result-with-feedbacks")
    if response.status_code == 404:
        raise HTTPException(status_code=404,
                            detail="No result found for assessment. Assessment might not be submitted.")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error on Artemis server: " + response.text)
    res_json = response.json()
    if "feedbacks" not in res_json:
        raise HTTPException(status_code=400,
                            detail="No feedbacks for assessment found. Assessment might not be submitted.")
    feedbacks = [ReceivedFeedback(f["text"], f["detailText"], f["credits"]) for f in res_json["feedbacks"] if
                 f["type"] == "MANUAL"]

    print("All found feedbacks:", feedbacks)

    method_feedbacks = []
    for filepath, content in files.items():
        methods: List[MethodNode] = extract_methods(content)
        for method in methods:
            start = method.start_line
            stop = method.stop_line
            for feedback in feedbacks:
                if feedback.file == filepath and feedback.from_line >= start and feedback.to_line <= stop:
                    method_feedbacks.append(
                        Feedback(
                            exercise_id=request.exercise_id,
                            participation_id=request.participation_id,
                            code=method.source_code,
                            src_file=filepath,
                            from_line=feedback.from_line,
                            to_line=feedback.to_line,
                            text=feedback.detailText,
                            credits=feedback.credits
                        )
                    )
    # remove feedbacks for this participation before inserting new ones
    db.delete_feedbacks(request.participation_id)
    db.store_feedbacks(method_feedbacks)

    print("Stored feedbacks", method_feedbacks)

    return "Success!"


class ReceivedFeedback:
    def __init__(self, text, detail_text, credits):
        self.text = text
        self.detailText = detail_text
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
        elif "at line" in self.text and "column" in self.text:
            line_num = int(self.text.split()[-3])
            return line_num, line_num
        elif "at line" in self.text:
            line_num = int(self.text.split()[-1])
            return line_num, line_num
        else:
            return 0, 0

    def __str__(self):
        return f"Feedback: {self.text} ({self.from_line}, {self.to_line})"

    def __repr__(self):
        return self.__str__()


@router.get("/feedback_suggestions/feedbacks")
def get_feedbacks():
    return db.fetch_feedbacks()


@router.get("/feedback_suggestions/feedbacks/{exercise_id}")
def get_feedbacks_for_exercise(exercise_id):
    return db.fetch_feedbacks_by_exercise_id(exercise_id)
