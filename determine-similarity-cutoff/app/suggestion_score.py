from typing import Callable, Dict

from .feedback_suggestion import FeedbackSuggestion

# for typing
suggestion_score_function = Callable[[FeedbackSuggestion], float]


def suggestion_score(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score


def suggestion_score_random(suggestion: FeedbackSuggestion) -> float:
    import random
    return random.random()


def suggestion_score_f3(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score_f3


def suggestion_score_f1_times_precision(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score * suggestion.precision_score


def suggestion_score_f3_times_precision(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score_f3 * suggestion.precision_score


suggestion_score_functions: Dict[str, suggestion_score_function] = {
    "f1": suggestion_score,
    "f3": suggestion_score_f3,
    "random": suggestion_score_random,
    "f1*precision": suggestion_score_f1_times_precision,
    "f3*precision": suggestion_score_f3_times_precision,
}
