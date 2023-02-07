from logging import getLogger
from typing import Dict, List, Union

from fastapi import APIRouter
from fastapi import Header
from pydantic import BaseModel

from .auth_token import get_auth_token
from .authenticated_request import AuthRequest
from ..database.feedback_suggestion_entity import FeedbackSuggestionEntity
from ..extract_methods.extract_methods import extract_methods
from ..extract_methods.method_node import MethodNode
from ..feedback_suggestion.feedback_suggestions import get_feedback_suggestions
from ..helpers.request_error_handling import check_artemis_response
from ..helpers.slash import ensure_leading_slash

db = FeedbackSuggestionEntity()
logger = getLogger(name="FeedbackSuggestionRequest")
router = APIRouter()


class FeedbackSuggestionsRequest(BaseModel):
    server: str
    exercise_id: int
    participation_id: int
    include_code: bool = False


@router.post("/feedback_suggestions")
def get_feedback_suggestions_endpoint(
        request: FeedbackSuggestionsRequest,
        authorization: Union[str, None] = Header()
):
    logger.debug("-" * 80)
    logger.info("Start getting feedback suggestions!")

    token = get_auth_token(authorization)

    # get all files of the submission and its contents (source code)
    auth_request = AuthRequest(token, request.server)
    response = auth_request.get(f"/repository/{request.participation_id}/files-content")
    check_artemis_response(response)
    files: dict = {name: content for name, content in response.json().items() if name.endswith(".java")}

    # generate function blocks from all files of the submission
    function_blocks: Dict[str, List[MethodNode]] = {
        ensure_leading_slash(filepath): extract_methods(content) for filepath, content in files.items()
    }

    db_feedbacks = db.fetch_feedbacks_by_exercise_id(request.exercise_id)
    # remove own participation
    db_feedbacks = [f for f in db_feedbacks if f.participation_id != request.participation_id]

    suggested_feedbacks = get_feedback_suggestions(
        function_blocks, db_feedbacks, include_code=request.include_code)

    return suggested_feedbacks
