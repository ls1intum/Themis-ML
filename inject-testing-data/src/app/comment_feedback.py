from typing import List

from .test_submissions import get_test_submission


# add a feedback by adding a comment with "// feedback: <feedback text>" to the submission

def get_comment_feedbacks(participation_id: int) -> List[dict]:
    """Create a random feedback for random lines in the submission"""
    submission = get_test_submission(participation_id)
    print("Submission:", submission)
    feedbacks = []
    for file_path, file_content in submission.items():
        if not file_path.name.endswith(".java"):
            continue
        for line_number, line in enumerate(file_content.splitlines()):
            if "// feedback:" in line:
                feedback_detail_test = line.split("// feedback:")[1].strip()
                feedbacks.append(
                    {
                        "text": f"File /{file_path} at line {line_number} some feedback",
                        "detailText": feedback_detail_test,
                        "credits": -1.0,
                        "type": "MANUAL",
                    }
                )
    print("Feedbacks for", id, feedbacks)
    return feedbacks
