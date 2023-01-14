GRANT ALL PRIVILEGES ON DATABASE feedback_suggestion_db TO feedback_suggestion_user;

CREATE TABLE IF NOT EXISTS developers (
  DEVELOPER_ID INT NOT NULL,
  FIRST_NAME varchar(250) NOT NULL,
  LAST_NAME varchar(250) NOT NULL,
  EMAIL varchar(250),
  PRIMARY KEY (DEVELOPER_ID)
);