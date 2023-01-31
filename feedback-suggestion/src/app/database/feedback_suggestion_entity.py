import os

from sqlalchemy import create_engine
from ..feedback_suggestion.feedback import Feedback
from typing import List


class FeedbackSuggestionEntity:

    def __init__(self):
        DB_USER = os.environ.get('DATABASE_USER', 'feedback_suggestion_user')
        DB_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'password')
        DB_HOST = os.environ.get('DATABASE_HOST', 'localhost')
        DB_PORT = os.environ.get('DATABASE_PORT', '5432')
        DB_NAME = os.environ.get('DATABASE_NAME', 'feedback_suggestion_db')
        db_link = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        self.engine = create_engine(db_link)

    def fetch_feedbacks(self):
        with self.engine.connect() as conn:
            result = conn.execute("SELECT * FROM feedbacks")
            all_feedbacks = result.fetchall()
            return all_feedbacks

    def fetch_feedbacks_by_exercise_id(self, exercise_id):
        with self.engine.connect() as conn:
            result = conn.execute("SELECT * FROM feedbacks WHERE exercise_id = %s", exercise_id)
            all_feedbacks = result.fetchall()
            return all_feedbacks

    def store_feedbacks(self, feedbacks: List[Feedback]):
        with self.engine.connect() as conn:
            for feedback in feedbacks:
                conn.execute(
                    "INSERT INTO feedbacks (exercise_id, participation_id, code, src_file, from_line, to_line, "
                    "feedback_text, credits) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (feedback.exercise_id, feedback.participation_id, feedback.code, feedback.src_file,
                     feedback.from_line, feedback.to_line, feedback.text, feedback.credits)
                )

    def delete_feedbacks(self, participation_id):
        with self.engine.connect() as conn:
            conn.execute("DELETE FROM feedbacks WHERE participation_id = %s", participation_id)
