from fastapi import Depends
from passlib.hash import md5_crypt
from config.db_config import ConfigDB
from typing import Self
import string
import random


class User:
    def __init__(self, email=None, password=None, name=None, forename=None, role=None, cookie=None):
        self.email = email
        self.password = password
        self.name = name
        self.forename = forename
        self.role = role
        self.cookie = cookie

    def verify_password(self, plain_password) -> str:
        parts = self.password.split("$")
        scheme, salt, stored_hash = parts[1], parts[2], parts[3]
        stored_hash = stored_hash.strip()
        new_hash = md5_crypt.using(salt=salt).hash(plain_password)
        return new_hash == f"${scheme}${salt}${stored_hash}"

    def get_user(self, cursor, id_users=None, email=None, cookie=None) -> Self | None:
        SQL_query = (
            f"SELECT email, password, name, forename, role, cookie FROM USERS WHERE 1 = 1"
        )
        if id_users is not None:
            SQL_query += f" AND idusers = '{id_users}' "
        if email is not None:
            SQL_query += f" AND email = '{email}' "
        if cookie is not None:
            SQL_query += f" AND cookie = '{cookie}'"
        print(SQL_query)
        cursor.execute(SQL_query)
        user_data = cursor.fetchone()
        if user_data:
            self.email = user_data["email"]
            self.password = user_data["password"]
            self.name = user_data["name"]
            self.forename = user_data["forename"]
            self.role = user_data["role"]
            self.cookie = user_data["cookie"]
            return self
        return None

    def get_current_user_role(self, cookie: str, cursor=Depends(ConfigDB().get_db_cursor())) -> int | None:
        user = self.get_user(cursor, cookie=cookie)
        if user:
            return user.role
        return None

    def insert_user(self, connector, cursor, email, password, name, forename) -> Self:
        cursor.execute(
            f"INSERT INTO users(email, password, name, forename, role, cookie) VALUES('{email}', '{password}', '{name}', '{forename}', 2, '')"
        )
        connector.commit()
        letters = string.ascii_lowercase
        cookie_value = "".join(random.choice(letters) for _ in range(255))
        self.set_cookie(connector, cursor, email, cookie_value)
        return User(email, password, name, forename, 2, cookie_value)

    # A voir où est-ce qu'on le range
    def set_cookie(self, connector, cursor, email, cookie_value) -> None:
        sql = f"UPDATE USERS SET cookie = '{cookie_value}' WHERE email = '{email}'"
        self.cookie = cookie_value
        cursor.execute(sql)
        connector.commit()
