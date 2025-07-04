CREATE TABLE IF NOT EXISTS USERS
(
    IdUser VARCHAR(64) NOT NULL PRIMARY KEY,
    Email VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Forename VARCHAR(255) NOT NULL,
    Password CHAR(255) NOT NULL,
    Cookie VARCHAR(255),
    Role INT NOT NULL
);

CREATE TABLE IF NOT EXISTS MODELS
(
    IdModel SERIAL NOT NULL PRIMARY KEY,
    Path VARCHAR(255) NOT NULL,
    Date TIMESTAMP NOT NULL,
    IdUser VARCHAR(64) REFERENCES USERS(IdUser)
);

CREATE TABLE IF NOT EXISTS DEVICES
(
    IdDevice VARCHAR(8) NOT NULL PRIMARY KEY,
    IdUser VARCHAR(64) REFERENCES USERS(IdUser)
);