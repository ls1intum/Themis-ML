import os

from sqlalchemy import create_engine


class FeedbackSuggestionEntity:

    def __init__(self):
        DB_USER = os.environ.get('DATABASE_USER', 'feedback_suggestion_user')
        DB_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'password')
        DB_HOST = os.environ.get('DATABASE_HOST', 'localhost')
        DB_PORT = os.environ.get('DATABASE_PORT', '5432')
        DB_NAME = os.environ.get('DATABASE_NAME', 'feedback_suggestion_db')
        db_link = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        self.engine = create_engine(db_link)

    def insert_name(self, first_name, last_name, email):
        with self.engine.connect() as conn:
            conn.execute("INSERT INTO developers (first_name, last_name, email) VALUES (%s, %s, %s)",
                         (first_name, last_name, email))
            print('Data inserted successfully')

    def fetch_name(self):
        with self.engine.connect() as conn:
            result = conn.execute("SELECT * FROM developers")
            all_devs = result.fetchall()
            print('Data fetched successfully')
            print(all_devs)
            return all_devs
