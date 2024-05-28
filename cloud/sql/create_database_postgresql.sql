CREATE DATABASE icarus_db;

CREATE TABLE IF NOT EXISTS USERS (
	IdUser SERIAL NOT NULL PRIMARY KEY,
	Email VARCHAR(255) NOT NULL,
	Name VARCHAR(255) NOT NULL,
	Forename VARCHAR(255) NOT NULL,
	password CHAR(255) NOT NULL,
	Cookie VARCHAR(255),
	Role INT NOT NULL
);

CREATE TABLE IF NOT EXISTS MODELS (
	IdModel SERIAL NOT NULL PRIMARY KEY,
	Path VARCHAR(255) NOT NULL,
	Date TIMESTAMP NOT NULL,
	IdUser SERIAL REFERENCES USERS(IdUser)
);
