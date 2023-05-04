from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Genre

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the genre data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from genre.csv"

    def handle(self, *args, **options):

        if Genre.objects.exists():
            print('category data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading genre data")

        # Code to load the data into database
        for row in DictReader(open(f'{settings.DATAFILE_DIRS}/genre.csv')):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genre.save()
