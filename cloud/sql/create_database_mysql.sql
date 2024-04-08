CREATE TABLE USERS
(
	Email VARCHAR(255) NOT NULL,
	Name VARCHAR(255) NOT NULL,
	Forename VARCHAR(255) NOT NULL,
	Role INT NOT NULL,
    Cookie VARCHAR(255),
	PRIMARY KEY (Email)
);

CREATE TABLE MODEL
(
    IdModel SERIAL NOT NULL,
	Path VARCHAR(255) NOT NULL,
	Date DATE NOT NULL,
	PRIMARY KEY (IdModel),
	FOREIGN KEY (Email) REFERENCES USER(Email)
);