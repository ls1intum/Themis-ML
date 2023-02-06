import json
from pathlib import Path
from typing import List

from app.feedback_suggestion import FeedbackSuggestion
from app.run_manual_comparison import run_manual_comparison

GIVEN_SUGGESTIONS_FILE_NAME = "suggestions.json"
ACCEPTED_SUGGESTIONS_FILE_NAME = "accepted.json"
REJECTED_SUGGESTIONS_FILE_NAME = "rejected.json"

if not Path(GIVEN_SUGGESTIONS_FILE_NAME).exists():
    print(f"No suggestions given yet. \
Create {GIVEN_SUGGESTIONS_FILE_NAME} with the contents of <server>/feedback_suggestions to start.")
    exit(0)

if not Path(ACCEPTED_SUGGESTIONS_FILE_NAME).exists():
    Path(ACCEPTED_SUGGESTIONS_FILE_NAME).write_text("[]")

if not Path(REJECTED_SUGGESTIONS_FILE_NAME).exists():
    Path(REJECTED_SUGGESTIONS_FILE_NAME).write_text("[]")


def load_suggestions(filename) -> List[FeedbackSuggestion]:
    with open(filename, "r") as f:
        suggestions = json.load(f)
    return [FeedbackSuggestion(**s) for s in suggestions]


def store_suggestions(filename, suggestions: List[FeedbackSuggestion]):
    with open(filename, "w") as f:
        json.dump([s.to_json() for s in suggestions], f)


def get_given_suggestions() -> List[FeedbackSuggestion]:
    return load_suggestions(GIVEN_SUGGESTIONS_FILE_NAME)


def remove_given_suggestion(suggestion: FeedbackSuggestion):
    given = load_suggestions(GIVEN_SUGGESTIONS_FILE_NAME)
    if suggestion in given:
        given.remove(suggestion)
        store_suggestions(GIVEN_SUGGESTIONS_FILE_NAME, given)


def add_accepted_suggestion(suggestion: FeedbackSuggestion):
    accepted = load_suggestions(ACCEPTED_SUGGESTIONS_FILE_NAME)
    accepted.append(suggestion)
    store_suggestions(ACCEPTED_SUGGESTIONS_FILE_NAME, accepted)
    remove_given_suggestion(suggestion)


def add_rejected_suggestion(suggestion: FeedbackSuggestion):
    rejected = load_suggestions(REJECTED_SUGGESTIONS_FILE_NAME)
    rejected.append(suggestion)
    store_suggestions(REJECTED_SUGGESTIONS_FILE_NAME, rejected)
    remove_given_suggestion(suggestion)


if __name__ == "__main__":
    run_manual_comparison(
        get_given_suggestions(),
        add_accepted_suggestion,
        add_rejected_suggestion,
        lambda: load_suggestions(ACCEPTED_SUGGESTIONS_FILE_NAME),
        lambda: load_suggestions(REJECTED_SUGGESTIONS_FILE_NAME)
    )
