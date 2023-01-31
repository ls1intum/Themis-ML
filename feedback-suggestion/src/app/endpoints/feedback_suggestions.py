from logging import getLogger
from typing import Dict, List

import torch
from code_bert_score import score
from fastapi import APIRouter
from pydantic import BaseModel

from .feedback_suggestion_request import get_feedbacks_for_exercise
from .authenticated_request import AuthRequest
from ..extract_methods.extract_methods import extract_methods
from ..extract_methods.method_node import MethodNode
from ..feedback_suggestion.feedback import Feedback

logger = getLogger(name="FeedbackSuggestionRequest")
router = APIRouter()
# TODO: define threshold for similarity
SIMILARITY_SCORE_THRESHOLD = 0.5


class FeedbackSuggestionsRequest(BaseModel):
    token: str
    server: str
    exercise_id: int
    participation_id: int
    include_code: bool = False


def get_feedback_suggestions_for_feedback_row(
        function_blocks: Dict[str, List[MethodNode]],
        feedback: Feedback,
        include_code: bool = False
):
    """Get feedback suggestions from comparisons between function blocks of a given submission
    and a single feedback row."""
    for filepath, methods in function_blocks.items():
        if feedback.src_file == filepath:
            for method in methods:
                # F1 is the similarity score, F3 is similar to F1 but with a higher weight for recall than precision
                precision, recall, F1, F3 = score(cands=[method.get_source_code()], refs=[feedback.code],
                                                  lang='java')
                similarity_score = float(torch.mean(F1))  # TODO: is this correct?
                if similarity_score >= SIMILARITY_SCORE_THRESHOLD:
                    print(f"Found similar code with similarity score {similarity_score}: {feedback}")
                    original_code = feedback["code"]
                    feedback_to_give = feedback.copy()
                    if include_code:
                        feedback_to_give["code"] = method.get_source_code()
                    else:
                        del feedback_to_give["code"]
                    feedback_to_give["from_line"] = method.get_start_line()
                    feedback_to_give["to_line"] = method.get_stop_line()
                    result_data = {
                        "feedback": feedback_to_give,
                        "similarity_score": similarity_score
                    }
                    if include_code:
                        result_data["originally_on_code"] = original_code
                    yield result_data


@router.post("/feedback_suggestion")
def get_feedback_suggestions(request: FeedbackSuggestionsRequest):
    logger.debug("-" * 80)
    logger.info("Start getting feedback suggestions!")

    # get all files of the submission and its contents (source code)
    auth_request = AuthRequest(request.token, request.server)
    response = auth_request.get(f"/repository/{request.participation_id}/files-content")
    files: dict = {name: content for name, content in response.json().items() if name.endswith(".java")}

    # generate function blocks from all files of the submission
    function_blocks: Dict[str, List[MethodNode]] = {}
    for filepath, content in files.items():
        function_blocks[filepath] = extract_methods(content)

    # get all feedbacks for the submission
    db_feedbacks = get_feedbacks_for_exercise(request.exercise_id)

    # compare feedbacks with function blocks
    suggested_feedbacks = []
    for feedback_row in db_feedbacks:
        if feedback_row.participation_id == request.participation_id:
            continue
        feedback = Feedback.from_dict(dict(feedback_row))
        suggested_feedbacks.extend(
            list(get_feedback_suggestions_for_feedback_row(
                function_blocks,
                feedback,
                include_code=request.include_code
            ))
        )

    return suggested_feedbacks
