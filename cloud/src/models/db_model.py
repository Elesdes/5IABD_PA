from dataclasses import dataclass


@dataclass
class DataBaseModel:
    dbname: str = ""
    user: str = ""
    password: str = ""
    host: str = "localhost"
    port: str = "5432"
