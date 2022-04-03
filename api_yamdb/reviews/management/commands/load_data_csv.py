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
    # Show this when the user types help
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
            # cur.executemany("INSERT INTO reviews_category (id, name, slug) VALUES (?, ?, ?);", to_db, )

            cur.executemany(query_str, to_db, )
            con.commit()
            con.close()

        import_csv('category.csv')
        import_csv('genre.csv')
        import_csv('titles.csv')
        import_csv('genre_title.csv')
        import_csv('review.csv')
        import_csv('comments.csv')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена'))



        # with open('static/data/category.csv') as csvfile:
        #     dict_reader = DictReader(csvfile)
        #     for row in dict_reader:
        #         category = Category(name=row['name'], slug=row['slug'])
        #         category.save()
        #
        # with open('static/data/genre.csv') as csvfile:
        #     dict_reader = DictReader(csvfile)
        #     for row in dict_reader:
        #         genre = Genre(name=row['name'], slug=row['slug'])
        #         genre.save()

        # with open('static/data/titles.csv') as csvfile:
        #     dict_reader = DictReader(csvfile)
        #     for row in dict_reader:
        #         title = Title(name=row['name'],
        #                       year=row['year'],
        #                       category=Category.objects.get(id=row['category']))
        #         title.save()

        # with open('static/data/genre_title.csv') as csvfile:
        #     dict_reader = DictReader(csvfile)
        #     for row in dict_reader:
        #         genre = Genre.objects.get(id=row['genre_id'])
        #         title = Title.objects.get(id=row['title_id'])
        #         title_genre(genre)
        #         title.save()
        #
        # with open('static/data/comments.csv') as csvfile:
        #     dict_reader = DictReader(csvfile)
        #     for row in dict_reader:
        #         comment = Comment(review=row['review_id'],
        #                           text=row['text'],
        #                           author=row['author'],
        #                           pub_date=row['pub_date'])
        #         comment.save()
        #
        # with open('static/data/review.csv') as csvfile:
        #     dict_reader = DictReader(csvfile)
        #     for row in dict_reader:
        #         review = Review(title=row['title_id'],
        #                         text=row['text'],
        #                         author=row['author'],
        #                         score=row['score'],
        #                         pub_date=row['pub_date']
        #         )
        #         review.save()

