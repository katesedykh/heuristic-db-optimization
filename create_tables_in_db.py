import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_table(connection, schema_name, table_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE TABLE {schema_name}.{table_name} (id serial PRIMARY KEY, name VARCHAR);")
        print(f"Table {schema_name}.{table_name} created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
    finally:
        cursor.close()

def grant_table_permissions(connection, schema_name, table_name, user_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"GRANT ALL PRIVILEGES ON TABLE {schema_name}.{table_name} TO {user_name};")
        print(f"Table-level permissions granted to {user_name} on {schema_name}.{table_name}")
    except Exception as e:
        print(f"An error occurred while granting table-level permissions: {e}")
    finally:
        cursor.close()

conn = psycopg2.connect(dbname="algo_project", user="postgres", password="123456789", host="localhost")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

try:
    create_table(conn, "public", "table1")
    create_table(conn, "public", "table2")

    # Grant permissions to mks_user on the public schema and the table
    grant_table_permissions(conn, "public", "table1", "mks_user")
    grant_table_permissions(conn, "public", "table2", "mks_user")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
