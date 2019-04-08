DROP TABLE IF EXISTS Groups;
DROP TABLE IF EXISTS Code_Iterations;
DROP TABLE IF EXISTS Compilations;
DROP TABLE IF EXISTS Processes;

CREATE TABLE Groups (
  id SERIAL,
  students TEXT[]
);

CREATE TABLE Code_Iterations (
  id SERIAL,
  group_id INT,
  code TEXT,
  time TIMESTAMP
);

CREATE TABLE Compilations (
  id SERIAL,
  group_id INT,
  code TEXT,
  output TEXT,
  error TEXT,
  time TIMESTAMP
);
