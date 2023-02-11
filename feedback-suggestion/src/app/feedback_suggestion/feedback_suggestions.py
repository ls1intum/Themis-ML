from multiprocessing import Pool, cpu_count
from typing import Dict, List, Iterator

from .code_similarity_computer import CodeSimilarityComputer
from .feedback import Feedback
from ..extract_methods.method_node import MethodNode

SIMILARITY_SCORE_THRESHOLD = 0.75


def get_feedback_suggestions_for_method(
        feedbacks: Iterator[Feedback],
        filepath: str,
        method: MethodNode,
        include_code: bool = False
):
    """Get feedback suggestions from comparisons between a function block of a given submission
    and multiple feedback rows"""
    considered_feedbacks = []
    sim_computer = CodeSimilarityComputer()
    for feedback in feedbacks:
        if feedback.src_file == filepath and feedback.method_name == method.name:
            considered_feedbacks.append(feedback)
            sim_computer.add_comparison(method.source_code, feedback.code)

    sim_computer.compute_similarity_scores()

    suggested = []
    for feedback in considered_feedbacks:
        similarity = sim_computer.get_similarity_score(method.source_code, feedback.code)
        if similarity.f1 >= SIMILARITY_SCORE_THRESHOLD:
            print(f"Found similar code with similarity score {similarity}: {feedback}")
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
                "precision_score": similarity.precision,
                "recall_score": similarity.recall,
                "similarity_score": similarity.f1,
                "similarity_score_f3": similarity.f3,
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
    # this needs to be called for the server not to shut down after the request
    pool.close()
    pool.join()
    return [result for result_list in results for result in result_list]
