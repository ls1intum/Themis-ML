import psycopg2
import os


class FeedbackSuggestionEntity:

    def __init__(self):
        DB_HOST = str(os.environ['DATABASE_HOST']) if "DATABASE_HOST" in os.environ else "postgres"
        DB_PORT = int(os.environ['DATABASE_PORT']) if "DATABASE_PORT" in os.environ else "5432"
        DB_NAME = str(os.environ['DATABASE_NAME']) if "DATABASE_NAME" in os.environ else "feedback_suggestion_db"
        DB_USER = str(os.environ['DATABASE_USER']) if "DATABASE_USER" in os.environ else "postgres_user"
        DB_PASS = str(os.environ['DATABASE_PASS']) if "DATABASE_PASS" in os.environ else "password"

        try:
            self.conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host="0.0.0.0", port=DB_PORT)
            print("Database connected successfully")
        except:
            print(DB_HOST)
            print(DB_PORT)
            print(DB_NAME)
            print(DB_USER)
            print(DB_PASS)
            print("Database not connected successfully")

    def insert_name(self, first_name, last_name, email):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO developers (FIRST_NAME,LAST_NAME,EMAIL) VALUES(%s, %s, %s)",
                    (first_name, last_name, email))
                    
        print('Data inserted successfully')
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
