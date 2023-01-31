from typing import Dict, List

import torch
from code_bert_score import score

from .feedback import Feedback

from ..extract_methods.method_node import MethodNode

# TODO: define threshold for similarity
SIMILARITY_SCORE_THRESHOLD = 0.5


def get_feedback_suggestions_for_feedback(
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
