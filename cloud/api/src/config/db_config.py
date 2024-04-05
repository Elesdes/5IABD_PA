from dataclasses import dataclass
import psycopg2
import os

from psycopg2.extras import RealDictCursor


@dataclass
class ConfigDB:
    connector: psycopg2.connect = None

    def __init__(self):
        self._get_connector()

    def _get_connector(self) -> None:
        try:
            self._get_local_connector()
            print('Connected to Local DB')

        except psycopg2.OperationalError as e:
            self._get_azure_connector()
            print('Connected to Azure')

        except Exception as e:
            print(f"Error not caught : {e}")

    def _get_local_connector(self) -> None:
        """
        Used in local to get local DB
        """
        conn = psycopg2.connect(
            dbname="icarus-pa-database",
            user="hqvdqqhguy",
            password="PYZLO1052XB6ZVPQ$",
            host="localhost"
        )
        self.connector = conn

    def _get_azure_connector(self) -> None:
        """
        Used in azure to get azure DB
        """
        connection_string = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
        connection = psycopg2.connect(connection_string)
        self.connector = connection

    def get_db_cursor(self) -> psycopg2:
        """
        Get current cursor to operate requests
        :return: cursor psycopg2 object
        """
        if self.connector is None:
            self._get_connector()
        cursor = self.connector.cursor(cursor_factory=RealDictCursor)
        return cursor
