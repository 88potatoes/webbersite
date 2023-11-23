from django.core.management.base import BaseCommand
from ...models import Article
import logging

logger = logging.getLogger(__name__)


"""clear all data and create new objects"""
MODE_REFRESH="refresh"

"""clear all data"""
MODE_CLEAR="clear"

class Command(BaseCommand):
    help="seed database for testing"

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")
        parser.add_argument('--noclear', type=bool, help="inclusion of '--noclear' will not clear the database before inserting new entries")

    def handle(self, *args, **options):
        # logger.info(args)
        # self.stdout.write(options['mode'])
        self.stdout.write("...seeding data.")
        run_seed(self, options["mode"], options["noclear"])
        self.stdout.write("done")

def create_article():
    """creates an article"""

    article = Article(title="new title", body="new body")
    article.save()
    logger.info("{} was created".format(article))
    return article

def run_seed(self, mode, noclear):
    if not noclear:
        clear_data()

    if mode == MODE_CLEAR:
        return
    
    for i in range(15):
        create_article()

def clear_data():
    """clears all data from the database"""
    logger.info("clearing database")
    Article.objects.all().delete()