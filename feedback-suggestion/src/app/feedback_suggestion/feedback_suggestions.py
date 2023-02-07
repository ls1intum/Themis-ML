import os
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Iterator

import torch
from code_bert_score import score

from .feedback import Feedback
from ..extract_methods.method_node import MethodNode

# TODO: define threshold for similarity
SIMILARITY_SCORE_THRESHOLD = 0.85


def equal_except_whitespace(s1: str, s2: str) -> bool:
    return "".join(s1.split()) == "".join(s2.split())


def get_model_params(lang: str) -> dict:
    if "ML_JAVA_MODEL" in os.environ:
        if os.path.exists(os.environ["ML_JAVA_MODEL"]):
            print("Using local model")
            return dict(model_type=os.environ["ML_JAVA_MODEL"])
        else:
            print("Local model not found, using default model")
    return dict(lang=lang)


def get_feedback_suggestions_for_method(
        feedbacks: Iterator[Feedback],
        filepath: str,
        method: MethodNode,
        include_code: bool = False
):
    """Get feedback suggestions from comparisons between a function block of a given submission
    and multiple feedback rows"""
    exact_match_feedbacks = []
    feedback_refs = []
    suggested = []
    for feedback in feedbacks:
        if feedback.src_file == filepath and feedback.method_name == method.name:
            if equal_except_whitespace(feedback.code, method.source_code):
                # no need to throw this into the ML machine,
                # we already know it's pretty much a perfect match
                exact_match_feedbacks.append(feedback)
            else:
                feedback_refs.append(feedback)
    candidates = [method.source_code] * len(feedback_refs)

    if len(candidates) == 0:
        return suggested

    # F1 is the similarity score, F3 is similar to F1 but with a higher weight for recall than precision
    precision, recall, F1, F3 = score(
        cands=candidates,
        refs=[f.code for f in feedback_refs],
        device=torch.device("mps"),  # TODO: only works on mac
        **get_model_params("java")
    )
    precision_scores = precision.tolist()
    similarity_scores_f1 = F1.tolist()
    similarity_scores_f3 = F3.tolist()

    # add perfect matches again
    feedback_refs.extend(exact_match_feedbacks)
    similarity_scores_f1.extend([1.0] * len(exact_match_feedbacks))
    similarity_scores_f3.extend([1.0] * len(exact_match_feedbacks))
    precision_scores.extend([1.0] * len(exact_match_feedbacks))

    for feedback, similarity_score_f1, similarity_score_f3, precision_score in zip(
            feedback_refs, similarity_scores_f1, similarity_scores_f3, precision_scores,
            strict=True
    ):
        if similarity_score_f1 >= SIMILARITY_SCORE_THRESHOLD:
            print(f"Found similar code with similarity score {similarity_score_f1}: {feedback}")
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
                "similarity_score": similarity_score_f1,
                "similarity_score_f3": similarity_score_f3,
                "precision_score": precision_score
            }
            if include_code:
                result_data["originally_on_code"] = original_code
            suggested.append(result_data)
    return sorted(suggested, key=lambda x: x["similarity_score"], reverse=True)


def get_feedback_suggestions(
        function_blocks: Dict[str, List[MethodNode]],
        feedbacks: Iterator[Feedback],
        include_code: bool = False
):
    """
    Get feedback suggestions from comparisons between function blocks of a given submission
    and multiple feedback rows.
    This is quicker than calling get_feedback_suggestions_for_method for each method
    because it uses multiple processes to do the comparisons in parallel.
    """
    pool = Pool(processes=cpu_count())
    results = pool.starmap(get_feedback_suggestions_for_method,
                           [
                               (feedbacks, filepath, method, include_code)
                               for filepath, methods in function_blocks.items()
                               for method in methods
                           ])
    return [result for result_list in results for result in result_list]
