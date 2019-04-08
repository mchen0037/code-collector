DROP TABLE IF EXISTS Groups;
DROP TABLE IF EXISTS Code_Iterations;
DROP TABLE IF EXISTS Compilations;

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
  output TEXT,
  time TIMESTAMP
);
