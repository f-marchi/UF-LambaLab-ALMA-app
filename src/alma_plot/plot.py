import re
from bs4 import BeautifulSoup
from .utils import *

def plot_alma(df, xaxis, yaxis,x_range, y_range,cols=[],save_html=False):
    
    source = ColumnDataSource(df)
    x = 'P(Death) at 5y'
    WIDTH = 1000
    THRESHOLD = 0.5

    risk_plot = create_risk_plot(source, WIDTH, x, THRESHOLD)
    histogram_plot = create_histogram_plot(df, source, WIDTH, x)

    tabs = []
    for col in cols:
        scatter_plot = create_scatter_plot(df, source, col, x_range, y_range, xaxis, yaxis)
        tabs.append(TabPanel(child=scatter_plot, title=col))

    tabs_control = Tabs(tabs=tabs, tabs_location='above')

    if save_html:
        from bokeh.plotting import output_file
        output_file("docs/index.html")

    layout = column(tabs_control, histogram_plot, risk_plot)

    return show(layout)

def modify_html(input_file, output_file):
    # Read the input HTML file
    with open(input_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Update the title
    soup.title.string = "Acute Leukemia Methylome Atlas"

    # Update the CSS styles
    style_tag = soup.find('style')
    new_styles = """
      html, body {
        box-sizing: border-box;
        height: 100%;
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
      }

      body {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        overflow-y: auto;
      }

      .container {
        width: 90%;
        max-width: 1200px;
        background-color: white;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        margin-bottom: 40px;
      }

      h1 {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
        color: #333;
      }

      #plot-container {
        width: 100%;
        max-height: 700px;
        overflow-y: auto;
      }

      /* Scrollbar customization */
      #plot-container::-webkit-scrollbar {
        width: 12px;
      }

      #plot-container::-webkit-scrollbar-thumb {
        background-color: #888;
        border-radius: 6px;
      }

      #plot-container::-webkit-scrollbar-thumb:hover {
        background-color: #555;
      }
    """
    style_tag.string = new_styles

    # Wrap the plot div in a container and add a title
    plot_div = soup.find('div', {'data-root-id': True})
    original_id = plot_div['id']
    plot_div['id'] = 'plot-container'
    container_div = soup.new_tag('div', attrs={'class': 'container'})
    h1_tag = soup.new_tag('h1')
    h1_tag.string = "Acute Leukemia Methylome Atlas"
    plot_div.wrap(container_div)
    container_div.insert(0, h1_tag)

    # Update the JavaScript to use the new plot-container id
    script_tag = soup.find('script', text=re.compile('embed_document'))
    script_content = script_tag.string
    script_content = re.sub(
        r'"roots":\{"([^"]+)":"[^"]+"\}',
        f'"roots":{{"\\1":"plot-container"}}',
        script_content
    )
    script_tag.string = script_content

    # Write the modified HTML to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))