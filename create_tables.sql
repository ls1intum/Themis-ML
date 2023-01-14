GRANT ALL PRIVILEGES ON DATABASE feedback_suggestion_db TO feedback_suggestion_user;

CREATE TABLE IF NOT EXISTS developers (
  DEVELOPER_ID SERIAL,
  FIRST_NAME varchar(250) NOT NULL,
  LAST_NAME varchar(250) NOT NULL,
  EMAIL varchar(250),
  PRIMARY KEY (DEVELOPER_ID)
);

CREATE TABLE IF NOT EXISTS feedbacks (
  id SERIAL PRIMARY KEY,
  exercise_id INT NOT NULL,
  participation_id INT NOT NULL,
  code TEXT NOT NULL,
  src_file TEXT NOT NULL,
  from_line INT NOT NULL,
  to_line INT NOT NULL,
  feedback_text TEXT NOT NULL,
  credits FLOAT NOT NULL
);

