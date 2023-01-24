import requests
from django.core.management.base import BaseCommand
from ...models import Paper
import json
import xmltodict

url = 'http://export.arxiv.org/api/query?search_query=cat:cs.PL&max_results=500'

def get_research_papers(url):
    """
    Gets the research papers by calling the Arxiv API.
    
    @param url: the URL corresponding to the Arxiv API
    @return: JSON containing the research papers
    """
    response = requests.get(url)
    data_dict = xmltodict.parse(response.text)
    json_data = json.dumps(data_dict)
    json_data = json.loads(json_data)

    return json_data['feed']['entry']


def seed(url):
    """
    Adds the rsearch papers to the database.
    """

    papers = get_research_papers(url)
    for paper in papers:
        
        if isinstance(paper['author'], dict):
            authors_name = paper['author']['name']
        else:
            authors_name = paper['author'][0]['name']
            
        pl_paper = Paper(abstract = paper['summary'],
                         title = paper['title'],
                         author = authors_name,
                         paper_url = paper['link'][0]['@href'],
                         published_date = paper['published'],
                         subject =  paper['arxiv:primary_category']['@term'],
                         updated = paper['updated'],
                         pdf_url = paper['link'][1]['@href'],)
        pl_paper.save()
    Paper.objects.all().order_by('id')


class Command(BaseCommand):
    def handle(self, *args, **options):
        seed(url)
        print("\nSeeding Completed.")
