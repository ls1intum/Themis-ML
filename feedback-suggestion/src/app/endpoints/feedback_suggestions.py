from logging import getLogger
from typing import Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

from .authenticated_request import AuthRequest
from .feedback_suggestion_request import get_feedbacks_for_exercise
from ..extract_methods.extract_methods import extract_methods
from ..extract_methods.method_node import MethodNode
from ..feedback_suggestion.feedback import Feedback
from ..feedback_suggestion.feedback_suggestions import get_feedback_suggestions_for_feedback

logger = getLogger(name="FeedbackSuggestionRequest")
router = APIRouter()


class FeedbackSuggestionsRequest(BaseModel):
    token: str
    server: str
    exercise_id: int
    participation_id: int
    include_code: bool = False


@router.post("/feedback_suggestion")
def get_feedback_suggestions(request: FeedbackSuggestionsRequest):
    logger.debug("-" * 80)
    logger.info("Start getting feedback suggestions!")

    # get all files of the submission and its contents (source code)
    auth_request = AuthRequest(request.token, request.server)
    response = auth_request.get(f"/repository/{request.participation_id}/files-content")
    files: dict = {name: content for name, content in response.json().items() if name.endswith(".java")}

    # generate function blocks from all files of the submission
    function_blocks: Dict[str, List[MethodNode]] = {
        filepath: extract_methods(content) for filepath, content in files.items()
    }

    # get all feedbacks for the submission
    db_feedbacks = get_feedbacks_for_exercise(request.exercise_id)

    # compare feedbacks with function blocks
    suggested_feedbacks = []
    for feedback_row in db_feedbacks:
        if feedback_row.participation_id == request.participation_id:
            continue
        suggested_feedbacks.extend(
            list(get_feedback_suggestions_for_feedback(
                function_blocks,
                Feedback.from_dict(dict(feedback_row)),
                include_code=request.include_code
            ))
        )

    return suggested_feedbacks
