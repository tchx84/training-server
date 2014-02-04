CREATE DATABASE training;

CREATE USER 'training'@'localhost' IDENTIFIED BY 'training';
GRANT ALL PRIVILEGES ON training . * TO 'training'@'localhost';
