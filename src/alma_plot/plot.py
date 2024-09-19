from .utils import *

def plot_alma(df, test_sample=None, 
              xaxis="PaCMAP 1 of 2", yaxis="PaCMAP 2 of 2",
              x_range=(-45, 45), y_range=(-45, 45), 
              cols=['AL Epigenomic Subtype','WHO 2022 Diagnosis','Hematopoietic Entity', 
                    'Vital Status', 'AML Epigenomic Risk', 
                    'Risk Group AAML1831', 'Clinical Trial',
                    'Race or ethnic group', 'Age (group years)'],
              save_html=False):
    
    source = ColumnDataSource(df)
    width = 1000
    x = 'P(Death) at 5y'
    threshold = 0.5

    risk_plot = create_risk_plot(df, source, width, x, threshold, test_sample)
    histogram_plot = create_histogram_plot(df, source, width, x)

    tabs = []
    for col in cols:
        scatter_plot = create_scatter_plot(df, source, col, x_range, y_range, xaxis, yaxis, test_sample)
        tabs.append(TabPanel(child=scatter_plot, title=col))

    tabs_control = Tabs(tabs=tabs, tabs_location='above')

    if save_html:
        from bokeh.plotting import output_file
        output_file("docs/index.html")

    layout = column(tabs_control, histogram_plot, risk_plot)

    return show(layout)