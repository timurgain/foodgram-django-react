import os
import psycopg2
import json
from typing import List
from dotenv import load_dotenv

load_dotenv()


def turn_json_to_list(file_path: str) -> List[dict]:
    """."""
    with open(file=file_path, mode='r', encoding='utf-8') as file:
        return json.load(file)


def write_ingredients_to_postgres(ingredients: List[dict]):
    """."""
    conn = None
    try:
        # create a connection to db
        conn = psycopg2.connect(
            host="localhost",
            database=os.getenv('DB_NAME'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'))
        print(f"Database connection established at {conn}")

        # create a cursor
        cur = conn.cursor()
        table = 'foodgram_ingredient'
        column1 = 'name'
        column2 = 'measurement_unit'

        sql_count = (f"SELECT COUNT ({column1}) FROM {table};")
        cur.execute(sql_count)
        results = cur.fetchone()[0]
        print("Database entries before loading:", results)

        for ingredient in ingredients:
            name = ingredient['name']
            measurement_unit = ingredient['measurement_unit']
            sql_insert = (
                f"INSERT INTO {table} ({column1}, {column2})"
                f" SELECT * FROM (SELECT '{name}' AS {column1}, '{measurement_unit}' AS {column2}) AS temp"
                f" WHERE NOT EXISTS (SELECT {column1} FROM {table} WHERE {column1} = '{name}') LIMIT 1;"
            )
            cur.execute(sql_insert)
            conn.commit()

        cur.execute(sql_count)
        results = cur.fetchone()[0]
        print("Database entries after loading:", results)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    ingredients = turn_json_to_list(file_path='data/ingredients.json')
    write_ingredients_to_postgres(ingredients)
    print('Well done')
