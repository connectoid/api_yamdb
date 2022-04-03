import csv
import sqlite3

from django.core.management import BaseCommand

from reviews.models import User

DB = 'db.sqlite3'
CSV_PATH = 'static/data/'
TABLES = {
    'category.csv': 'reviews_category',
    'genre.csv': 'reviews_genre',
    'titles.csv': 'reviews_title',
    'genre_title.csv': 'reviews_title_genre',
    'review.csv': 'reviews_review',
    'comments.csv': 'reviews_comment',
    'users.csv': 'reviews_user',
}


class Command(BaseCommand):
    help = "Loads data from csv"

    def handle(self, *args, **options):

        with open('static/data/users.csv', 'r', encoding='utf-8') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                user = User(username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'])
                user.save()

        def import_csv(filename):

            con = sqlite3.connect(DB)
            cur = con.cursor()

            with open(CSV_PATH + filename, 'r', encoding='utf-8') as file:
                values = csv.DictReader(file, delimiter=",")
                fields = values.fieldnames
                to_db = []
                for row in values:
                    to_db.append([row[col] for col in fields])
            count = len(fields)
            table_name = TABLES[filename]
            query_str = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({('?, ' * count)[:-2]});"

            cur.executemany(query_str, to_db,)
            con.commit()
            con.close()

        import_csv('category.csv')
        import_csv('genre.csv')
        import_csv('titles.csv')
        import_csv('genre_title.csv')
        import_csv('review.csv')
        import_csv('comments.csv')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена'))
