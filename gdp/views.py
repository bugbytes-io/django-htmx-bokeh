from django.db.models import Max, Min
from django.shortcuts import render
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

from .models import GDP
from . import plotting

# Create your views here.
def index(request):
    # define a year
    max_min_year = GDP.objects.aggregate(
        max_yr=Max('year'),
        min_yr=Min('year')
    )
    year = request.GET.get('year', max_min_year['max_yr'])
    print(year)

    # define number of countries to fetch
    count = int(request.GET.get('count', 10))
    
    # extract data for that year for top N
    gdps = GDP.objects.filter(year=year).order_by('gdp').reverse()[:count]

    # country names
    country_names = [d.country for d in gdps]
    country_gdps = [d.gdp for d in gdps]
    cds = ColumnDataSource(data=dict(country_names=country_names, country_gdps=country_gdps))

    fig = figure(x_range=country_names, height=500, title=f"Top {count} GDPs ({year})")

    # styling
    plotting.base_styles(fig)

    # create the bar chart
    fig.vbar(x='country_names', top='country_gdps', width=0.8, source=cds)

    # Add the HoverTool to the figure
    tooltips = [
        ('Country', '@country_names'),
        ('GDP', '@country_gdps{,}')
    ]
    fig.add_tools(HoverTool(tooltips=tooltips))

    script, div = components(fig)

    context = {
        'script': script, 
        'div': div,
        'years': range(max_min_year['min_yr'], max_min_year['max_yr']+1),
        'year_selected': year,
        'count': count
    }
    
    if request.htmx:
        return render(request, 'partials/gdp-bar.html', context)
    return render(request, 'index.html', context)