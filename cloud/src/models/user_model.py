from fastapi import Depends
from passlib.hash import md5_crypt
from src.utils.postgresql_utils import PostgreSQLUtils
from typing import Self
import psycopg2
import string
import random


class User:
    def __init__(
        self,
        email: str = None,
        password: str = None,
        name: str = None,
        forename: str = None,
        role: int = None,
        cookie: int = None,
    ):
        self.email = email
        self.password = password
        self.name = name
        self.forename = forename
        self.role = role
        self.cookie = cookie

    def verify_password(self, plain_password: str) -> str:
        parts = self.password.split("$")
        scheme, salt, stored_hash = parts[1], parts[2], parts[3]
        stored_hash = stored_hash.strip()
        new_hash = md5_crypt.using(salt=salt).hash(plain_password)
        return new_hash == f"${scheme}${salt}${stored_hash}"

    def get_user(
        self,
        cursor: psycopg2,
        id_users: int = None,
        email: str = None,
        cookie: str = None,
    ) -> Self | None:
        parameters = list()
        SQL_query = f"SELECT email, password, name, forename, role, cookie FROM USERS WHERE 1 = 1"
        if id_users is not None:
            SQL_query += " AND idusers = %s "  # f" AND idusers = '{id_users}' "
            parameters.append(id_users)
        if email is not None:
            SQL_query += " AND email = %s "  #  f" AND email = '{email}' "
            parameters.append(email)
        if cookie is not None:
            SQL_query += " AND cookie = %s"  #f" AND cookie = '{cookie}'"
            parameters.append(cookie)
        if len(parameters) > 0:
            cursor.execute(SQL_query, parameters)
        else:
            cursor.execute(SQL_query)
        user_data = cursor.fetchone()
        if user_data:
            self.email = user_data[0]
            self.password = user_data[1]
            self.name = user_data[2]
            self.forename = user_data[3]
            self.role = user_data[4]
            self.cookie = user_data[5]
            return self
        return None

    def get_current_user_role(
        self, cookie: str, cursor=Depends(PostgreSQLUtils())
    ) -> int | None:
        user = self.get_user(cursor, cookie=cookie)
        if user:
            return user.role
        return None

    def insert_user(
        self,
        cursor: psycopg2,
        email: str,
        password: str,
        name: str,
        forename: str,
    ) -> Self:
        cursor.execute(
            f"INSERT INTO USERS(email, password, name, forename, role, cookie) VALUES('{email}', '{password}', '{name}', '{forename}', 2, '')"
        )
        letters = string.ascii_lowercase
        cookie_value = "".join(random.choice(letters) for _ in range(255))
        self.set_cookie(cursor, email, cookie_value)
        return User(email, password, name, forename, 2, cookie_value)

    # A voir où est-ce qu'on le range
    def set_cookie(
        self,
        cursor: psycopg2,
        email: str,
        cookie_value: str,
    ) -> None:
        sql = f"UPDATE USERS SET cookie = '{cookie_value}' WHERE email = '{email}'"
        self.cookie = cookie_value
        cursor.execute(sql)
