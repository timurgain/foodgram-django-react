# https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/
import json
import os
from typing import Any, List, Optional

from django.core.management.base import (BaseCommand, CommandError,
                                         CommandParser)

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = 'Write ingredients from .json to postgres.'

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        ingredients = self.turn_json_to_list('data/ingredients.json')
        self.write_ingredients_to_postgres(self, ingredients=ingredients)
        self.stdout.write(self.style.SUCCESS('Well done'))

    @staticmethod
    def turn_json_to_list(file_path: str) -> List[dict]:
        with open(file=file_path, mode='r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def write_ingredients_to_postgres(self, ingredients: List[dict]):
        conn = None
        try:
            # create a connection to db
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'))
            self.stdout.write(self.style.SUCCESS(
                f"Database connection established at {conn}"))

            # create a cursor
            cur = conn.cursor()
            table = 'foodgram_ingredient'
            column1 = 'name'
            column2 = 'measurement_unit'

            sql_count = (f"SELECT COUNT ({column1}) FROM {table};")
            cur.execute(sql_count)
            results = cur.fetchone()[0]
            self.stdout.write(self.style.SUCCESS(
                f"Database entries before loading: {results}"))

            for ingredient in ingredients:
                name = ingredient['name']
                measurement_unit = ingredient['measurement_unit']
                sql_insert = (
                    f"INSERT INTO {table} ({column1}, {column2})"
                    f" SELECT * FROM (SELECT '{name}' AS {column1},"
                    f" '{measurement_unit}' AS {column2}) AS temp"
                    f" WHERE NOT EXISTS (SELECT {column1} FROM {table}"
                    f" WHERE {column1} = '{name}') LIMIT 1;"
                )
                cur.execute(sql_insert)
                conn.commit()

            cur.execute(sql_count)
            results = cur.fetchone()[0]
            self.stdout.write(self.style.SUCCESS(
                f'Database entries after loading: {results}'))
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            raise CommandError(error)
        finally:
            if conn is not None:
                conn.close()
                self.stdout.write(self.style.SUCCESS(
                    'Database connection closed'))
