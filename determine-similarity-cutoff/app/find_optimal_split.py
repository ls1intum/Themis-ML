from typing import List, Tuple

from .feedback_suggestion import FeedbackSuggestion
from .suggestion_score import suggestion_score_function


def find_optimal_split(
        accepted: List[FeedbackSuggestion],
        rejected: List[FeedbackSuggestion],
        score_from_suggestion: suggestion_score_function
) -> Tuple[float, float]:
    """
    Find the optimal split between accepted and rejected suggestions.
    The optimal split is a score such that the sum of
    - the number of accepted suggestions with a score higher than the split
    - the number of rejected suggestions with a score lower than the split
    is maximized.

    :returns: a tuple (optimal_split_score, max_points)
    """
    if not accepted and not rejected:
        return 0.5, 0

    accepted_scores = [score_from_suggestion(suggestion) for suggestion in accepted]
    rejected_scores = [score_from_suggestion(suggestion) for suggestion in rejected]

    # The optimal split score is one of the scores in accepted_scores or rejected_scores.
    # We can find the optimal split score by iterating over all scores and checking the
    # points = (#accepted with score > split) + (#rejected with score < split)
    def get_split_score_points(split_score: float) -> int:
        accept_points = sum([int(score > split_score) for score in accepted_scores])
        reject_points = sum([int(score < split_score) for score in rejected_scores])
        return accept_points + reject_points

    max_points = None
    optimal_split_score = None
    for score in accepted_scores + rejected_scores:
        points = get_split_score_points(score)
        if max_points is None or points > max_points:
            max_points = points
            optimal_split_score = score

    return optimal_split_score, max_points
