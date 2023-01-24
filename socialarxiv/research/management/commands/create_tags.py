from django.core.management.base import BaseCommand
from ...models import Paper
from textblob import TextBlob

def create_tags():
    papers = Paper.objects.all()
    for paper in papers:
        summary = paper.abstract
        blob = TextBlob(summary)
        nouns = blob.noun_phrases
        for noun in nouns:
            paper.tags.add(noun)


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_tags()
        print("\nSeeding Completed.")
