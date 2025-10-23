-- Drop tables if they already exit
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS report;

-- Create the user table
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- Create the report table
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
--   severity TEXT CHECK ( severity IN ('Info','Low','Medium','High','Critical')),
--   mitigation TEXT,
--   status TEXT DEFAULT 'Open' CHECK ( severity IN ('Open','In Review','On Hold','Resolved','Closed')),
  FOREIGN KEY (author_id) REFERENCES user (id)
);