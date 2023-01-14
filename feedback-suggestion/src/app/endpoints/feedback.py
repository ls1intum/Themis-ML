from dataclasses import dataclass

@dataclass
class Feedback:
    exercise_id: int
    participation_id: int
    code: str
    src_file: str
    from_line: int
    to_line: int
    text: str
    credits: float