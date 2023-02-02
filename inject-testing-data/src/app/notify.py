import os

import requests

THEMIS_URL = os.environ.get("THEMIS_URL", "http://localhost:8000")
TEST_SERVER_URL = os.environ.get("TEST_SERVER_URL", "http://localhost:8001") + "/inject"


def notify_themis_ml(exercise_id: int, participation_id: int):
    """Notify the ML service about a new submission."""
    resp = requests.post(
        f"{THEMIS_URL}/feedback_suggestion/notify",
        json={
            "exercise_id": exercise_id,
            "participation_id": participation_id,
            "server": TEST_SERVER_URL,
        },
        headers={
            "Authorization": "Bearer not_needed",
        }
    )
    resp.raise_for_status()
