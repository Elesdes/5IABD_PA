# ICARUS - 5AIBD Annual Project 2023-2024

ICARUS is an open-source student project aimed at developing a system for controlling a non-invasive 3D-printed hand prosthesis through EMG signals using deep reinforcement learning algorithms, thereby exploring the interactions between technology and the human body by leveraging concepts related to human-machine interactions.

## Install PostgreSQL and the BDD

In order to connect the website to our BDD, you need to have either a cloud structure connected to it or a local installation. We will explain how to install PostgreSQL and how to feed the database and the structure.

## Project Setup

Make sure to read the first README.md of the project. It is required to have a proper interpreter environment to call the database.

### Download and install PostgreSQL

Go to the official website of PostgreSQL and download the latest app wizard.

[PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

Follow the instructions and don't tick off any choices.
You'll need to set a password to your admin profile. Please be cautious while choosing it.
Let anything by default.
You don't need Stack builder to install anything else.

### Create the database

Open pgAdmin4. Click on "Servers" in the left list. Write your password previously set.
Right click Login/Group Roles -> Create -> Login/Group Roles. Create your user. Please be careful, you'll need to accept "Can login?" Privileges.
Click on "Object" -> Create -> Database... Name your database and set your user as the owner.
Click on your newly created database. On the top left of the app, click Query Tool.
Copy and paste to query tool and execute the file : `cloud/sql/create_database_postgresql.sql`

## Authors

- [Erwan DUPREY](https://github.com/ErwanDuprey)
- [Enzo LEONARDO](https://github.com/Leonardeaux)
- [Juan MAUBRAS](https://github.com/Elesdes)
