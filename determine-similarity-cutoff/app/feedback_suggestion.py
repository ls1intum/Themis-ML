from dataclasses import dataclass


@dataclass
class FeedbackSuggestion:
    id: int
    exercise_id: int
    participation_id: int
    method_name: str
    code: str
    originally_on_code: str
    src_file: str
    from_line: int
    to_line: int
    text: str
    credits: float
    similarity_score: float
    similarity_score_f3: float
    precision_score: float
    recall_score: float = 0.0

    def to_json(self):
        return {
            "id": self.id,
            "exercise_id": self.exercise_id,
            "participation_id": self.participation_id,
            "method_name": self.method_name,
            "code": self.code,
            "originally_on_code": self.originally_on_code,
            "src_file": self.src_file,
            "from_line": self.from_line,
            "to_line": self.to_line,
            "text": self.text,
            "credits": self.credits,
            "similarity_score": self.similarity_score,
            "similarity_score_f3": self.similarity_score_f3,
            "precision_score": self.precision_score,
            "recall_score": self.recall_score,
        }
