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

    @staticmethod
    def from_dict(data: dict):
        return Feedback(
            exercise_id=data["exercise_id"],
            participation_id=data["participation_id"],
            code=data["code"],
            src_file=data["src_file"],
            from_line=data["from_line"],
            to_line=data["to_line"],
            text=data.get("text", ""),
            credits=data["credits"]
        )

    def to_dict(self):
        return {
            "exercise_id": self.exercise_id,
            "participation_id": self.participation_id,
            "code": self.code,
            "src_file": self.src_file,
            "from_line": self.from_line,
            "to_line": self.to_line,
            "text": self.text,
            "credits": self.credits
        }