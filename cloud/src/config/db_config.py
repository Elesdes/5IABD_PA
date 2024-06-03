from src.models.db_model import DataBaseModel
import os

config_db = DataBaseModel(
    dbname=os.getenv("CLOUD_SQL_DATABASE_NAME"),
    user=os.getenv("CLOUD_SQL_USERNAME"),
    password=os.getenv("CLOUD_SQL_PASSWORD"),
    host=os.getenv("CLOUD_PRIVATE_IP"),
    port=os.getenv("PORT"),
)
