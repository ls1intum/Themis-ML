import os
import requests


THEMIS_URL = os.environ.get("THEMIS_URL", "http://localhost:8000")
TEST_SERVER_URL = os.environ.get("TEST_SERVER_URL", "http://localhost:8001")


def notify_themis_ml(id: int):
    """Notify the ML service about a new submission."""
    resp = requests.post(
        f"{THEMIS_URL}/feedback_suggestion/notify",
        json={
            "token": "not_needed",
            "exercise_id": id,
            "participation_id": id,
            "server": TEST_SERVER_URL,
        },
    )
    resp.raise_for_status()
