from csv import DictReader
from django.core.management import BaseCommand

# Import the model
from reviews.models import User, Category, Title, Genre, Comment, Review


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from csv"

    def handle(self, *args, **options):

        for row in DictReader(open('../../../static/data/users.csv')):
            user = User(username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name'])
            user.save()

        for row in DictReader(open('../../../static/data/category.csv')):
            category = Category(name=row['name'], slug=row['slug'])
            category.save()

        for row in DictReader(open('../../../static/data/genre.csv')):
            genre = Genre(name=row['name'], slug=row['slug'])
            genre.save()

        for row in DictReader(open('../../../static/data/titles.csv')):
            title = Title(name=row['name'],
                          year=row['year'],
                          categories=row['category'])
            title.save()

        for row in DictReader(open('../../../static/data/genre_title.csv')):
            genre = Genre.objects.get(id=row['genre_id'])
            title = Title.objects.get(id=row['title_id'])
            title.genre(genre)
            title.save()

        for row in DictReader(open('../../../static/data/comments.csv')):
            comment = Comment(review=row['review_id'],
                              text=row['text'],
                              author=row['author'],
                              pub_date=row['pub_date'])
            comment.save()

        for row in DictReader(open('../../../static/data/review.csv')):
            review = Review(title=row['title_id'],
                            text=row['text'],
                            author=row['author'],
                            score=row['score'],
                            pub_date=row['pub_date']
            )
            review.save()






