from fastapi import Depends
from passlib.hash import md5_crypt
from passlib.context import CryptContext
from src.utils.postgresql_utils import PostgreSQLUtils
from typing import Self
import psycopg2
import string
import random


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    def get_user_by_id(
        self,
        cursor: psycopg2,
        id_users: int = None,
    ) -> Self | None:
        if id_users is None:
            return None
        SQL_query = f"SELECT email, password, name, forename, role, cookie FROM USERS WHERE idusers = %s"
        cursor.execute(SQL_query, (id_users, ))
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

    def get_user_by_email(
            self,
            cursor: psycopg2,
            email: str = None,
    ) -> Self | None:
        if email is None:
            return None
        SQL_query = f"SELECT email, password, name, forename, role, cookie FROM USERS WHERE email = %s"
        cursor.execute(SQL_query, (email,))
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

    def get_user_by_cookie(
            self,
            cursor: psycopg2,
            cookie: str = None,
    ) -> Self | None:
        if cookie is None:
            return None
        SQL_query = f"SELECT email, password, name, forename, role, cookie FROM USERS WHERE cookie = %s"
        cursor.execute(SQL_query, (cookie,))
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
        user = self.get_user_by_cookie(cursor, cookie=cookie)
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
        request_str = "INSERT INTO USERS(idusers, email, password, name, forename, role, cookie) VALUES(%s %s, %s, %s, %s, 2, '')"
        cursor.execute(
            request_str, (pwd_context.hash(email), email, password, name, forename)
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
        sql = f"UPDATE USERS SET cookie = %s WHERE email = %s"
        self.cookie = cookie_value
        cursor.execute(sql, (cookie_value, email))
