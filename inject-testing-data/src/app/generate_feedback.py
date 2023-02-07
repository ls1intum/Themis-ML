import re
from typing import List

from .test_submissions import get_test_submission

# add a feedback by adding a comment with "// feedback: <feedback text>" to the submission
# Change this to your needs. If you want feedback on all Java methods, you could use the regex from
# https://stackoverflow.com/a/847507/4306257 (without the r modifier on the string)
FEEDBACK_REGEX = "(public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])"
# You can use the following placeholders in the feedback text:
#   $0: The whole regex match
#   $1: The first group of the regex match
#   $2: The second group of the regex match
#   ...
#   $file_name: The name of the file where the match was found
FEEDBACK_TEXT = "some feedback"


def generate_feedback(participation_id: int) -> List[dict]:
    """Searches for the regex in the submission code and generates feedbacks for each match using the feedback text.
    You can only match within one line.
    """
    submission = get_test_submission(participation_id)
    print("Submission:", submission)
    feedbacks = []
    for file_path, file_content in submission.items():
        if not file_path.name.endswith(".java"):
            continue
        for line_number, line in enumerate(file_content.splitlines()):
            if re.search(FEEDBACK_REGEX, line):
                groups = re.search(FEEDBACK_REGEX, line).groups()
                feedback_text = FEEDBACK_TEXT.replace("$file_name", file_path.name)
                for i, group in enumerate(groups, start=1):
                    feedback_text = feedback_text.replace(f"${i}", group)
                feedbacks.append(
                    {
                        "text": f"File {file_path} at line {line_number + 1}",
                        "detailText": feedback_text,
                        "credits": -1.0,
                        "type": "MANUAL",
                    }
                )
    print("Feedbacks for", participation_id, feedbacks)
    return feedbacks
