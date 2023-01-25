"""
A test submission is a ZIP file in a subdirectory of the test-submissions
directory. We will base64-encode the paths to use as a kind of participation
ID and convert back and forth between the two.
"""
from pathlib import Path
import glob

TEST_SUBMISSIONS_DIR = Path("test-submissions")


# Submission paths look like "test-submissions/1-2" (exercise 1, participation 2).

def get_test_submission_path(participation_id) -> Path:
    """Convert a participation ID to a path to a test submission."""
    return next(TEST_SUBMISSIONS_DIR.glob(f"*-{participation_id}"))


def get_exercise_id(path: Path) -> int:
    """Convert a path to a test submission to an exercise ID."""
    return int(path.name.split("-")[0])


def get_participation_id(path: Path) -> int:
    """Convert a path to a test submission to a participation ID."""
    return int(path.name.split("-")[1])


def get_test_submissions(exercise_id: int) -> list[Path]:
    """Get a list of all test submissions in the exercise."""
    str_paths = glob.glob(f"{TEST_SUBMISSIONS_DIR}/{exercise_id}-*")
    return [Path(path) for path in str_paths]


def get_participation_ids(exercise_id: int) -> list[int]:
    return [
        get_participation_id(path)
        for path in get_test_submissions(exercise_id)
    ]


def get_test_submission(participation_id: int) -> dict:
    """Get a test submission, which is a dictionary of relative
    filepaths to file contents."""
    submission_path = get_test_submission_path(participation_id)
    files = {}
    for name in submission_path.glob("**/*"):
        if name.as_posix().startswith("__MACOSX/"):
            continue
        if name.name in [".DS_Store", "Thumbs.db"]:
            continue
        if not name.name.endswith(".java"):
            # TODO: Handle other file types.
            continue
        if name.is_file():
            with open(name, "r", encoding="latin-1") as f:
                relative_path = name.relative_to(submission_path)
                files[relative_path] = f.read()
    return files
