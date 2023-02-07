GRANT ALL PRIVILEGES ON DATABASE feedback_suggestion_db TO feedback_suggestion_user;

CREATE TABLE IF NOT EXISTS feedbacks (
  id SERIAL PRIMARY KEY,
  exercise_id INT NOT NULL,
  participation_id INT NOT NULL,
  method_name TEXT NOT NULL,
  code TEXT NOT NULL,
  src_file TEXT NOT NULL,
  from_line INT NOT NULL,
  to_line INT NOT NULL,
  text TEXT NOT NULL,
  credits FLOAT NOT NULL
);

