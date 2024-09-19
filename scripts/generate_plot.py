import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.append(src_dir)

import pandas as pd
from alma_plot.plot import plot_alma

def main():

    # Load dataset
    df = pd.read_excel('../ALMA/data/alma_main_results.xlsx')

    # Prognostic model samples
    df_px = df[~df['Vital Status at 5y'].isna()]
    df_px_ = df_px.sort_values(by='P(Death) at 5y').reset_index().reset_index(names=['Percentile']).set_index('index')
    df_px_['Percentile'] = df_px_['Percentile'] / len(df_px_['Percentile'])
    df2 = df.join(df_px_[['Percentile']])

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
        df2,
        xaxis=xaxis,
        yaxis=yaxis,
        x_range=x_range,
        y_range=y_range,
        cols=cols,
        save_html=True
    )

    print("ALMA plot generated successfully!")

if __name__ == "__main__":
    main()