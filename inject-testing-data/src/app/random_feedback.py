import random
from typing import List

from .test_submissions import get_test_submission


def get_random_feedbacks(id: int) -> List[dict]:
    """Create a random feedback for random lines in the submission"""
    submission = get_test_submission(id)
    print("Submission:", submission)
    feedbacks = []
    for file_path, file_content in submission.items():
        if not file_path.name.endswith(".java"):
            continue
        if file_path.name == "BinarySearch.java":
            for line_number, line in enumerate(file_content.splitlines()):
                if "return -2;" in line and "// there will be feedback for this" in line:
                    feedbacks.append(
                        {
                            "text": f"File /{file_path} at line {line_number} some feedback",
                            "detailText": f"You should return -1",
                            "credits": -1.0,
                            "type": "MANUAL",
                        }
                    )
    print("Feedbacks for", id, feedbacks)
    return feedbacks
