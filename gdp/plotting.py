import math
from bokeh.models import NumeralTickFormatter

def base_styles(fig):
    fig.title.align = 'center'
    fig.title.text_font_size = '1.5em'
    fig.yaxis[0].formatter = NumeralTickFormatter(format="$0.0a")

    fig.xaxis.major_label_orientation = math.pi / 4