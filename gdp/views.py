from django.db.models import Max, Min
from django.shortcuts import render
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter

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

    # country names and GDPs
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

def line(request):
    countries = GDP.objects.values_list('country', flat=True).distinct()
    country = request.GET.get('country', 'Germany')

    gdps = GDP.objects.filter(country=country).order_by('year')

    year_data = []
    gdp_data = []
    c = ['Germany', 'China', 'France']

    for country in c:
        gdps = GDP.objects.filter(country=country).order_by('year')
        country_years = year_data.append([d.year for d in gdps])
        country_gdps = gdp_data.append([d.gdp for d in gdps])

    cds = ColumnDataSource(data=dict(
        country_years=year_data, 
        country_gdps=gdp_data,
        names=c,
        colors=['red', 'blue', 'green']
    ))

    fig = figure(height=500, title=f"{country} GDP")
    fig.title.align = 'center'
    fig.title.text_font_size = '1.5em'
    fig.yaxis[0].formatter = NumeralTickFormatter(format="$0.0a")

    fig.multi_line(
        source=cds, 
        xs='country_years', 
        ys='country_gdps', 
        line_width=2,
        legend_group='names',
        line_color='colors')

    fig.legend.location = 'top_left'

    script, div = components(fig)

    context = {
        'countries': countries,
        'country': country,
        'script': script, 
        'div': div,
    }

    if request.htmx:
        return render(request, 'partials/gdp-bar.html', context)
    return render(request, 'line.html', context)