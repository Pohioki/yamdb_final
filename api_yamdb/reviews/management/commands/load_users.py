from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import User

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the user data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from users.csv"

    def handle(self, *args, **options):

        if User.objects.exists():
            print('title data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading user data")

        # Code to load the data into database
        for row in DictReader(
                open(f'{settings.DATAFILE_DIRS}/users.csv')):
            title = User(id=row['id'],
                         username=row['username'],
                         email=row['email'],
                         role=row['role'],
                         bio=row['bio'],
                         first_name=row['first_name'],
                         last_name=row['last_name'])
            title.save()
