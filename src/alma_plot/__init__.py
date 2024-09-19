# Import main functions from plot.py
from .plot import plot_alma, modify_html

# Import utility functions from utils.py
from .utils import (
    get_custom_color_palette,
    create_risk_plot,
    create_histogram_plot,
    create_scatter_plot
)

# Define what should be available when using "from package import *"
__all__ = [
    'plot_alma',
    'get_custom_color_palette',
    'create_risk_plot',
    'create_histogram_plot',
    'create_scatter_plot',
    'modify_html'
]