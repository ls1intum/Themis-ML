from typing import Callable, List

from .feedback_suggestion import FeedbackSuggestion

# for typing
suggestion_score_function = Callable[[FeedbackSuggestion], float]


def suggestion_score(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score


def suggestion_score_f3(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score_f3


def suggestion_score_precision(suggestion: FeedbackSuggestion) -> float:
    return suggestion.precision_score


def suggestion_score_f1_times_lines_of_code(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score * (suggestion.to_line - suggestion.from_line)


def suggestion_score_f3_times_lines_of_code(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score_f3 * (suggestion.to_line - suggestion.from_line)


suggestion_score_functions: List[suggestion_score_function] = [
    suggestion_score,
    suggestion_score_f3,
    suggestion_score_precision,
    suggestion_score_f1_times_lines_of_code,
    suggestion_score_f3_times_lines_of_code,
]
