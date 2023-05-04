from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Title

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the title data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from titles.csv"

    def handle(self, *args, **options):

        if Title.objects.exists():
            print('title data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading title data")

        # Code to load the data into database
        for row in DictReader(
                open(f'{settings.DATAFILE_DIRS}/titles.csv')):
            title = Title(id=row['id'],
                          name=row['name'],
                          year=row['year'],
                          category_id=row['category'])
            title.save()
