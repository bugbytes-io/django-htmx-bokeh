import json
from itertools import dropwhile

from django.conf import settings
from django.core.management.base import BaseCommand
from gdp.models import GDP

class Command(BaseCommand):
    help = 'Load Courses and Modules'

    def handle(self, *args, **kwargs):
        # Add GDP objects, if there are none in the DB
        if not GDP.objects.count():
            datafile = settings.BASE_DIR / 'data' / 'gdp.json'
            
            # read in data from the JSON file
            with open(datafile, 'r') as f:
                data = json.load(f)

            data = dropwhile(lambda x: x['Country Name'] != 'Afghanistan', data)

            gdps = []
            for d in data:
                gdps.append(GDP(
                    country=d['Country Name'],
                    country_code=d['Country Code'],
                    gdp=d['Value'],
                    year=d['Year']
                ))

            GDP.objects.bulk_create(gdps)

        