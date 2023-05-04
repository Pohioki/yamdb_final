from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import GenreTitle

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the genre_title data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from genre_title.csv"

    def handle(self, *args, **options):

        if GenreTitle.objects.exists():
            print('genre_title data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading genre_title data")

        # Code to load the data into database
        for row in DictReader(
                open(f'{settings.DATAFILE_DIRS}/genre_title.csv')
        ):
            genre_title = GenreTitle(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id'])
            genre_title.save()
