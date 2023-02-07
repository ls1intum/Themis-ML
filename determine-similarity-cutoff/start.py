import json
from pathlib import Path
from typing import List

import dataset

from app.feedback_suggestion import FeedbackSuggestion
from app.run_manual_comparison import run_manual_comparison

GIVEN_SUGGESTIONS_FILE_NAME = "suggestions.json"
GIVEN_SUGGESTIONS_DB_NAME = "suggestions.sqlite"

db = dataset.connect(f"sqlite:///{GIVEN_SUGGESTIONS_DB_NAME}")
suggestions = db["suggestions"]
accepted = db["accepted"]
rejected = db["rejected"]

if Path(GIVEN_SUGGESTIONS_FILE_NAME).exists():
    print("Loading suggestions from JSON into the database for faster operations...")
    with open(GIVEN_SUGGESTIONS_FILE_NAME, "r") as f:
        suggestions_json = json.load(f)
    for s in suggestions_json:
        suggestions.insert(s)
    Path(GIVEN_SUGGESTIONS_FILE_NAME).unlink()


def load_suggestions(table_name) -> List[FeedbackSuggestion]:
    return [FeedbackSuggestion(**s) for s in db[table_name].all()]


def insert_suggestion(table_name, suggestion: FeedbackSuggestion):
    db[table_name].upsert(suggestion.to_json(), ["id"])


def remove_given_suggestion(suggestion: FeedbackSuggestion):
    suggestions.delete(
        exercise_id=suggestion.exercise_id,
        participation_id=suggestion.participation_id,
        method_name=suggestion.method_name
    )


def add_accepted_suggestion(suggestion: FeedbackSuggestion):
    insert_suggestion("accepted", suggestion)
    remove_given_suggestion(suggestion)


def add_rejected_suggestion(suggestion: FeedbackSuggestion):
    insert_suggestion("rejected", suggestion)
    remove_given_suggestion(suggestion)


if __name__ == "__main__":
    run_manual_comparison(
        load_suggestions("suggestions"),
        add_accepted_suggestion,
        add_rejected_suggestion,
        lambda: load_suggestions("accepted"),
        lambda: load_suggestions("rejected")
    )
