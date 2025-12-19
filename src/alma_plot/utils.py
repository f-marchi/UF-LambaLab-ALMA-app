import numpy as np
import pandas as pd
from bokeh.layouts import column
from bokeh.plotting import figure, show
from bokeh.models import (
    ColumnDataSource, CategoricalColorMapper, HoverTool,
    Label, GroupFilter, CDSView, Legend, LegendItem, Tabs, TabPanel,
    CustomJS, LabelSet, Span
)

font_size = '9pt'
width = 1200

def get_custom_color_palette():
    return [
        '#ff7f0e', '#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#7f7f7f',
        '#e377c2', '#e7ba52', '#bcbd22', '#17becf', '#393b79', '#8c564b',
        '#f7b6d2', '#c49c94', '#a2769e', '#dbdb8d', '#9edae5', '#c5b0d5',
        '#c7c7c7', '#ff9896', '#637939', '#aec7e8', '#ffbb78', '#98df8a',
        '#7c231e', '#3d6a3d', '#f96502', '#6d3f7d', '#6b4423', '#d956a6'
    ]
def create_risk_plot(source, x, threshold):
    p = figure(title='AML Epigenomic Risk', width=width, height=300,
               tools="xbox_select,reset,save", active_drag='xbox_select',
               x_axis_label=x, y_axis_label="Patient Percentile")
    p.toolbar.logo = None

    p.quad(left=0.15, right=threshold, bottom=0, top=1, color="#1f77b4", level="underlay", alpha=0.2)
    p.quad(left=threshold, right=0.85, bottom=0, top=1, color="#ff7f0e", level="underlay", alpha=0.2)

    for label_text, x_pos, color, align in [('High Risk', threshold + 0.01, '#ff7f0e', 'left'),
                                            ('Low Risk', threshold - 0.01, '#1f77b4', 'right')]:
        p.add_layout(Label(y=0.05, x=x_pos, text=label_text, text_font_size=font_size,
                           text_color=color, text_alpha=0.8, text_align=align))

    scatter = p.circle(x, 'Percentile', source=source, color="steelblue", alpha=0.1, 
                       size=7, hover_alpha=0.6, line_color=None, hover_fill_color="midnightblue",
                       hover_line_color="white", selection_color="midnightblue", selection_alpha=0.8,
                       selection_line_color="white")

    p.add_tools(HoverTool(renderers=[scatter], mode='vline', tooltips=None))

    return p

def create_histogram_plot(df, source, x):
    p = figure(title='AML Epigenomic Risk - Select clusters on the map and their prognosis will appear here', 
               width=width, height=300, x_axis_label=x, y_axis_label='Frequency', tools="save,reset")
    p.toolbar.logo = None

    hist, edges = np.histogram(df[x], bins=50, range=[0.15, 0.85])
    hist_source = ColumnDataSource(data=dict(top=hist, left=edges[:-1], right=edges[1:]))
    p.quad(top='top', bottom=0, left='left', right='right', source=hist_source, fill_color="navy", line_color="white", alpha=0.5)

    callback = CustomJS(args=dict(source=source, hist_source=hist_source, edges=edges, p=p), code="""
        const indices = source.selected.indices;
        const data = source.data;
        const hist_data = hist_source.data;

        const hist = new Array(edges.length - 1).fill(0);
        let sum_p_death = 0;

        for (let i = 0; i < indices.length; i++) {
            const idx = indices[i];
            const value = data['P(Death) at 5y'][idx];
            sum_p_death += value;
            for (let j = 0; j < edges.length - 1; j++) {
                if (value >= edges[j] && value < edges[j + 1]) {
                    hist[j] += 1;
                    break;
                }
            }
        }

        hist_data['top'] = hist;
        hist_source.change.emit();
        p.request_render();
    """)

    source.selected.js_on_change('indices', callback)

    return p

def create_scatter_plot(df, source, col, x_range, y_range, xaxis, yaxis):
    factors = [str(val) for val in df[col].unique() if pd.notnull(val)]
    color_mapper = CategoricalColorMapper(factors=factors, palette=get_custom_color_palette())

    p = figure(title='', width=width, height=810,
               tools="pan,wheel_zoom,box_select,reset,save", tooltips=[(str(col), '@{' + str(col) + '}')], 
               x_axis_label=xaxis, y_axis_label=yaxis,
               active_drag="box_select", x_range=x_range, y_range=y_range)

    p.toolbar.logo = None
    p.toolbar_location = 'above'

    for axis in [p.xaxis, p.yaxis]:
        axis.axis_label_text_font_size = font_size
        axis.axis_label_text_font_style = "normal"

    for factor in factors:
        view = CDSView(filter=GroupFilter(column_name=col, group=factor))
        p.scatter(x=xaxis, y=yaxis, source=source, view=view, 
                  color={'field': col, 'transform': color_mapper}, size=3, alpha=0.8, radius=0.2)

    legend = Legend(items=[LegendItem(label=factor, renderers=[r]) for factor, r in zip(factors, p.renderers)],
                    location="top", click_policy="hide",
                    label_text_font_size=font_size, label_text_font_style="normal",
                    glyph_height=15, glyph_width=15, spacing=1)

    p.add_layout(legend, 'right')

    return p