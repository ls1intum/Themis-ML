from logging import getLogger
from pydantic import BaseModel
from typing import Dict, List
from .authenticated_request import AuthRequest
from ..extract_methods.extract_methods import extract_methods
from ..extract_methods.method_node import MethodNode
from ..endpoints.FeedbackSuggestionRequest import FeedbackSuggestionRequest
from fastapi import APIRouter, HTTPException
from code_bert_score import score

logger = getLogger(name="FeedbackSuggestionRequest")
router = APIRouter()
# TODO: define threshold for similarity
SIMILARITY_SCORE_THRESHOLD = 0.5

class FeedbackSuggestionsRequest(BaseModel):
    token: str
    server: str
    exercise_id: int
    participation_id: str


@router.get("/feedback_suggestion")
def get_feedback_suggestions(self, request: FeedbackSuggestionsRequest):
    logger.debug("-" * 80)
    logger.info("Start getting feedback suggestions!")

    # get all files of the submission and its contents (source code)
    auth_request = AuthRequest(request.token, request.server)
    response = auth_request.get(f"/repository/{request.participation_id}/files-content")
    files: dict = { name: content for name, content in response.json().items() if name.endswith(".java") }

    # generate function blocks from all files of the submission
    function_blocks: Dict[str, List[MethodNode]]
    for filepath, content in files.items():
        function_blocks[filepath] = extract_methods(content)
    
    # get all feedbacks for the submission
    db_feedbacks = FeedbackSuggestionRequest.get_feedbacks_for_exercise(request.exercise_id)
    
    # compare feedbacks with function blocks
    suggestedFeedbacks = []
    for filepath, methods in function_blocks:
        for feedback in db_feedbacks:
            if feedback.filepath == "/" + filepath:
                for method in methods:
                    # F1 is the similarity score, F3 is similar to F1 but with a higher weight for recall than precision
                    precision, recall, F1, F3 = score(cands=method, refs=feedback.code, lang='java')
                    if (F1 >= SIMILARITY_SCORE_THRESHOLD):
                        suggestedFeedbacks.append(feedback)
    
    return suggestedFeedbacks
