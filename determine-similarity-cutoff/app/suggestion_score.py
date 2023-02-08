import random
from typing import Callable, Dict

from .feedback_suggestion import FeedbackSuggestion

# for typing
suggestion_score_function = Callable[[FeedbackSuggestion], float]


def suggestion_score(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score


def suggestion_score_f3(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score_f3


def suggestion_score_f1_times_precision(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score * suggestion.precision_score


def suggestion_score_f3_times_precision(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score_f3 * suggestion.precision_score


def suggestion_score_f1_times_recall(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score * suggestion.recall_score


def suggestion_score_f3_times_recall(suggestion: FeedbackSuggestion) -> float:
    return suggestion.similarity_score_f3 * suggestion.recall_score


def suggestion_score_random(suggestion: FeedbackSuggestion) -> float:
    return random.random()


suggestion_score_functions: Dict[str, suggestion_score_function] = {
    "f1": suggestion_score,
    "f3": suggestion_score_f3,
    "f1*precision": suggestion_score_f1_times_precision,
    "f3*precision": suggestion_score_f3_times_precision,
    "f1*recall": suggestion_score_f1_times_recall,
    "f3*recall": suggestion_score_f3_times_recall,
    "random": suggestion_score_random,
}
