from src.config.db_config import ConfigDB


def db_vars(func):
    def wrapper(*args, **kwargs):
        DB = ConfigDB()
        cursor = DB.get_db_cursor()

        val = func(DB, cursor, *args, **kwargs)

        cursor.close()
        DB.connector.close()
        return val

    return wrapper
