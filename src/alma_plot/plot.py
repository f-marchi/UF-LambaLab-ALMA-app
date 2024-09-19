import re
from bs4 import BeautifulSoup
from .utils import *

def plot_alma(df, xaxis, yaxis,x_range, y_range,cols=[],save_html=False):
    
    source = ColumnDataSource(df)
    x = 'P(Death) at 5y'
    THRESHOLD = 0.5

    risk_plot = create_risk_plot(source, x, THRESHOLD)
    histogram_plot = create_histogram_plot(df, source, x)

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
import re
from bs4 import BeautifulSoup


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
        background: linear-gradient(135deg, #e6e9f0 0%, #eef1f5 100%);
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
        padding: 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border-radius: 15px;
        margin-bottom: 40px;
      }

      .header {
        text-align: center;
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 1px solid #e0e0e0;
      }

      h1 {
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #333;
      }

      .subtitle {
        font-size: 18px;
        color: #666;
      }

      #plot-container {
        width: 100%;
        max-height: 700px;
        overflow-y: auto;
        margin-bottom: 40px;
        padding-bottom: 30px;
        border-bottom: 1px solid #e0e0e0;
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

      .button-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 30px;
        padding-top: 20px;
      }

      .button {
        display: inline-block;
        padding: 12px 24px;
        background-color: #4a6fa5;
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        border-radius: 5px;
        transition: all 0.3s ease;
        border: none;
      }

      .button:hover {
        background-color: #5a7fb5;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      }

      .footer {
        text-align: center;
        margin-top: 20px;
        font-size: 14px;
        color: #666;
      }
    """
    style_tag.string = new_styles

    # Wrap the plot div in a container and add a title and subtitle
    plot_div = soup.find('div', {'data-root-id': True})
    original_id = plot_div['id']
    plot_div['id'] = 'plot-container'
    container_div = soup.new_tag('div', attrs={'class': 'container'})
    header_div = soup.new_tag('div', attrs={'class': 'header'})
    h1_tag = soup.new_tag('h1')
    h1_tag.string = "Acute Leukemia Methylome Atlas"
    subtitle_tag = soup.new_tag('p', attrs={'class': 'subtitle'})
    subtitle_tag.string = "An open-source effort to define clinical subtypes of acute leukemias by epigenomics"
    header_div.append(h1_tag)
    header_div.append(subtitle_tag)
    plot_div.wrap(container_div)
    container_div.insert(0, header_div)

    # Add the three buttons
    button_container = soup.new_tag('div', attrs={'class': 'button-container'})
    buttons = [
        ('Docs', 'https://f-marchi.github.io/ALMA/'),
        ('Contribute', 'https://github.com/f-marchi/ALMA'),
        ('Dataset', 'https://github.com/f-marchi/ALMA/raw/refs/heads/main/data/alma_main_results.xlsx')
    ]
    for text, url in buttons:
        button = soup.new_tag('a', href=url, attrs={'class': 'button'})
        button.string = text
        button_container.append(button)
    container_div.append(button_container)

    # Add the copyright footnote
    footer = soup.new_tag('div', attrs={'class': 'footer'})
    footer.string = "Marchi et al. | Lamba Lab | University of Florida | © Copyright 2024"
    container_div.append(footer)

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