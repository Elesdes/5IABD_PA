import os
import psycopg2
from config.db_config import config_db
from models.db_model import DataBaseModel


class PostgreSQLUtils:
    def __init__(self, config: DataBaseModel = config_db):
        self.config = config.__dict__

    def __enter__(self):
        """
        Establish a database connection and return the cursor.
        This method is called when entering the context (using 'with' statement).
        """
        if connection_string := os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING"):
            self.conn = psycopg2.connect(connection_string)
        else:
            self.conn = psycopg2.connect(**self.config)
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Commit the transaction, close the cursor and connection.
        This method is called upon exiting the context.
        """
        self.conn.commit()
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":
    db_utils = PostgreSQLUtils()

    with db_utils as cur:
        cur.execute("SELECT * FROM users")
        print(cur.fetchall())