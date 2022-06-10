import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def write_json_to_sql():
    """."""
    conn = None
    try:
        # create a connection to db
        conn = psycopg2.connect(
            host="localhost",
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('USER_PASSWORD'))
        print(conn)

        # create a cursor
        cur = conn.cursor()
        db_version = cur.execute('SELECT version()')
        print(f'PostgreSQL database version: {db_version}')

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    write_json_to_sql()
