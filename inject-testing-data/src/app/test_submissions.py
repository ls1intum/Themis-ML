"""
A test submission is a ZIP file in a subdirectory of the test-submissions
directory. We will base64-encode the paths to use as a kind of participation
ID and convert back and forth between the two.
"""
from pathlib import Path
import glob
import zipfile

TEST_SUBMISSIONS_DIR = Path("test-submissions")


def get_test_submission_path(id: int) -> Path:
    """Convert a participation ID to a path to a test submission."""
    # This does not take security into account! Do not run this server
    # on a public network.
    return TEST_SUBMISSIONS_DIR / Path(id.to_bytes((id.bit_length() + 7) // 8, "big").decode())


def get_participation_id(path: Path) -> int:
    """Convert a path to a test submission to a participation ID."""
    return int.from_bytes(path.relative_to(TEST_SUBMISSIONS_DIR).as_posix().encode(), "big")


def get_test_submissions() -> list[Path]:
    """Get a list of all test submissions."""
    str_paths = glob.glob(f"{TEST_SUBMISSIONS_DIR}/**/*.zip", recursive=True)
    return [Path(path) for path in str_paths]


def get_test_submission_ids() -> list[int]:
    """Get a list of all test submission IDs."""
    return [get_participation_id(path) for path in get_test_submissions()]


def get_test_submission(id: int) -> dict:
    """Get a test submission, which is a dictionary of relative
    filepaths to file contents."""
    zip_path = get_test_submission_path(id)
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        return {name: zip_file.read(name).decode("latin-1") for name in zip_file.namelist() if ".git" not in name}
