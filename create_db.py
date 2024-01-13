import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(dbname="postgres", user="postgres", password="123456789", host="localhost") #superuser defined in installation
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

try:
    cur = conn.cursor()

    # Create a new database
    cur.execute("CREATE DATABASE algo_project;")

    # Create a new user
    cur.execute("CREATE USER mks_user WITH ENCRYPTED PASSWORD '123456789';")

    # Grant privileges to the user on the new database
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE algo_project TO mks_user;")

    cur.close()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
