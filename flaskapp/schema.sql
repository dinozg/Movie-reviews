-- schema.sql file

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS review;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  fullname TEXT NOT NULL
);

CREATE TABLE review (
  id INTEGER PRIMARY KEY,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);