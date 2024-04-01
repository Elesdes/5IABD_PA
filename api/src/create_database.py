import os
import psycopg2

connection_string = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
connection = psycopg2.connect(connection_string)
print("Connection established")

with connection.cursor() as cursor:
    cursor.execute(open("../../create_database_postgresql.sql", "r").read())

connection.commit()
connection.close()
