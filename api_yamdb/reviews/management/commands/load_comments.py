from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand
# Import the model
from reviews.models import Comment

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the comment data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from comments.csv"

    def handle(self, *args, **options):

        # Show this if the data already exist in the database
        if Comment.objects.exists():
            print('comment data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading comment data")

        # Code to load the data into database
        for row in DictReader(
                open(f'{settings.DATAFILE_DIRS}/comments.csv')):
            comment = Comment(
                review_id=row['review_id'],
                author_id=row['author'],
                text=row['text'],
                pub_date=row['pub_date'])
            comment.save()
