import psycopg
import os


class FeedbackSuggestionEntity:

    def __init__(self):
        dbhost = str(os.environ['DATABASE_HOST']) if "DATABASE_HOST" in os.environ else "postgres"
        dbport = int(os.environ['DATABASE_PORT']) if "DATABASE_PORT" in os.environ else 5432
        dbname = str(os.environ['DATABASE_NAME']) if "DATABASE_NAME" in os.environ else "feedback_suggestion_db"
        dbuser = str(os.environ['DATABASE_USER']) if "DATABASE_USER" in os.environ else "postgres_user"
        dbpass = str(os.environ['DATABASE_PASS']) if "DATABASE_PASS" in os.environ else "password"

        self.conn = psycopg.connect("dbname=feedback_suggestion_db user=postgres_user")
        print("Database connected successfully")

    def insert_name(self, first_name, last_name, email):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO developers (FIRST_NAME,LAST_NAME,EMAIL) VALUES(%s, %s, %s)",
                    (first_name, last_name, email))
        self.conn.commit()
        self.conn.close()

    def fetch_name(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM developers")
        cur.fetchone()
        for record in cur:
            print(record)

        print('Data fetched successfully')
        self.conn.commit()
        self.conn.close()

        return cur
