CREATE DATABASE flask_app;

USE flask_app;

CREATE TABLE user(
  uid INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(20),
  email VARCHAR(320),
  pwd VARCHAR(60) /* Consider using bcrypt */
);