from typing import Callable, Dict

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


suggestion_score_functions: Dict[str, suggestion_score_function] = {
    "f1": suggestion_score,
    "f3": suggestion_score_f3,
    "precision": suggestion_score_precision,
    "f1*lines": suggestion_score_f1_times_lines_of_code,
    "f3*line": suggestion_score_f3_times_lines_of_code,
}
