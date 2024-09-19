import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.append(src_dir)

import pandas as pd
from alma_plot.plot import plot_alma

def main():
    # Load your data
    print(f'directory: {os.getcwd()}')
    df = pd.read_excel('../ALMA/data/alma_main_results.xlsx')

    # Define plot parameters
    xaxis = "PaCMAP 1 of 2"
    yaxis = "PaCMAP 2 of 2"
    x_range = (-45, 45)
    y_range = (-45, 45)
    cols = [
        'AL Epigenomic Subtype',
        'WHO 2022 Diagnosis',
        'Hematopoietic Entity',
        'Vital Status',
        'AML Epigenomic Risk',
        'Risk Group AAML1831',
        'Clinical Trial',
        'Race or ethnic group',
        'Age (group years)'
    ]

    # Generate the plot
    plot_alma(
        df,
        xaxis=xaxis,
        yaxis=yaxis,
        x_range=x_range,
        y_range=y_range,
        cols=cols,
        save_html=True  # Set to True if you want to save the plot as an HTML file
    )

    print("ALMA plot generated successfully!")

if __name__ == "__main__":
    main()