-- create the main databases
CREATE DATABASE IF NOT EXISTS Spanglish;

-- create the test databases
CREATE DATABASE IF NOT EXISTS test;
 
-- create the test for the test database
CREATE USER 'test'@'%' IDENTIFIED BY '';
GRANT CREATE, ALTER, INDEX, LOCK TABLES, REFERENCES, UPDATE, DELETE, DROP, SELECT, INSERT ON `test`.* TO 'test'@'%';
 
FLUSH PRIVILEGES;