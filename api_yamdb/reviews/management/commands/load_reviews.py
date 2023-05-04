from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import Review

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the review data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from review.csv"

    def handle(self, *args, **options):

        if Review.objects.exists():
            print('category data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading category data")

        # Code to load the data into database
        for row in DictReader(
                open(f'{settings.DATAFILE_DIRS}/review.csv')):
            review = Review(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date']
            )
            review.save()
