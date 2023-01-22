import random
from typing import List

from .test_submissions import get_test_submission


def get_random_feedbacks(id: int) -> List[dict]:
    """Create a random feedback for random lines in the submission"""
    submission = get_test_submission(id)
    feedbacks = []
    number_of_feedbacks_left = random.randint(0, 10)
    submission_items = list(submission.items())
    random.shuffle(submission_items)
    for file_path, file_content in submission_items:
        if not file_path.endswith(".java"):
            continue
        lines = file_content.splitlines()
        line_numbers_with_java_methods = [i for i, line in enumerate(lines) if "public" in line]
        random.shuffle(line_numbers_with_java_methods)
        for line_number in line_numbers_with_java_methods:
            feedbacks.append({
                "text": f"File /{file_path} at line {line_number} some feedback",
                "detailText": f"File /{file_path} at line {line_number} some feedback",
                "credits": random.randint(-20, 20) / 2,
                "type": "MANUAL",
            })
            number_of_feedbacks_left -= 1
            if number_of_feedbacks_left <= 0:
                return feedbacks
    return feedbacks
