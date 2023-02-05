import os
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Iterator

import torch
from code_bert_score import score

from .feedback import Feedback
from ..extract_methods.method_node import MethodNode

# TODO: define threshold for similarity
SIMILARITY_SCORE_THRESHOLD = 0.85


def get_model_params(lang: str) -> dict:
    if "ML_JAVA_MODEL" in os.environ:
        if os.path.exists(os.environ["ML_JAVA_MODEL"]):
            print("Using local model")
            return dict(model_type=os.environ["ML_JAVA_MODEL"])
        else:
            print("Local model not found, using default model")
    return dict(lang=lang)


def get_feedback_suggestions_for_feedback(
        function_blocks: Dict[str, List[MethodNode]],
        feedback: Feedback,
        include_code: bool = False
):
    """Get feedback suggestions from comparisons between function blocks of a given submission
    and a single feedback row."""
    suggested = []
    for filepath, methods in function_blocks.items():
        if feedback.src_file == filepath:
            for method in methods:
                # F1 is the similarity score, F3 is similar to F1 but with a higher weight for recall than precision
                precision, recall, F1, F3 = score(
                    cands=[method.source_code],
                    refs=[feedback.code],
                    **get_model_params("java")
                )
                similarity_score = float(torch.mean(F1))  # TODO: is this correct?
                if similarity_score >= SIMILARITY_SCORE_THRESHOLD:
                    print(f"Found similar code with similarity score {similarity_score}: {feedback}")
                    original_code = feedback.code
                    feedback_to_give = feedback.to_dict()
                    if include_code:
                        feedback_to_give["code"] = method.source_code
                    else:
                        del feedback_to_give["code"]
                    feedback_to_give["from_line"] = method.start_line
                    feedback_to_give["to_line"] = method.stop_line
                    result_data = {
                        **feedback_to_give,
                        "similarity_score": similarity_score
                    }
                    if include_code:
                        result_data["originally_on_code"] = original_code
                    suggested.append(result_data)
    return suggested


def get_feedback_suggestions_for_multiple_feedbacks(
        function_blocks: Dict[str, List[MethodNode]],
        feedbacks: Iterator[Feedback],
        include_code: bool = False
):
    """
    Get feedback suggestions from comparisons between function blocks of a given submission
    and multiple feedback rows.
    This is quicker than calling get_feedback_suggestions_for_feedback for each feedback row
    because it uses multiple processes to do the comparisons in parallel.
    """
    pool = Pool(processes=cpu_count())
    results = pool.starmap(get_feedback_suggestions_for_feedback,
                           [(function_blocks, feedback, include_code) for feedback in feedbacks])
    return [result for result_list in results for result in result_list]
