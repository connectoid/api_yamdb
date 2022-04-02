from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import User, Category, Title, Genre, Comment, Review


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from csv"

    def handle(self, *args, **options):
        print('hi')
        with open('../static/data/users.csv') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                user = User(username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'])
                user.save()
        with open('../static/data/category.csv') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                category = Category(name=row['name'], slug=row['slug'])
                category.save()

        with open('../static/data/genre.csv') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                genre = Genre(name=row['name'], slug=row['slug'])
                genre.save()
        with open('../static/data/titles.csv') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                title = Title(name=row['name'],
                              year=row['year'],
                              categories=row['category'])
                title.save()
        with open('../static/data/genre_title.csv') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                genre = Genre.objects.get(id=row['genre_id'])
                title = Title.objects.get(id=row['title_id'])
                title.genre(genre)
                title.save()

        with open('../static/data/comments.csv') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                comment = Comment(review=row['review_id'],
                                  text=row['text'],
                                  author=row['author'],
                                  pub_date=row['pub_date'])
                comment.save()

        with open('../static/data/review.csv') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                review = Review(title=row['title_id'],
                                text=row['text'],
                                author=row['author'],
                                score=row['score'],
                                pub_date=row['pub_date']
                )
                review.save()






