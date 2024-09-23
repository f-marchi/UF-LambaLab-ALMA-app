# Acute Leukemia Methylome Atlas (ALMA)

## Notice

This is a pre-publication repository! Please consider all information here confidential and do not use any of the data or code until it has been peer-reviewed and published.

## Overview

The Acute Leukemia Methylome Atlas (ALMA) is an open-source project aimed at defining clinical subtypes of acute leukemias through epigenomics. This project provides a comprehensive tool for researchers and clinicians to explore and analyze methylation patterns in acute leukemia samples.

## Features

- Interactive visualization of acute leukemia methylation data
- Clustering and classification of leukemia subtypes based on methylation profiles
- Integration with clinical data for improved diagnostic and prognostic insights
- User-friendly web interface for easy data exploration

## Getting Started

### Prerequisites

- Python 3.10
- Bokeh 3.3.4
- BeautifulSoup4

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/f-marchi/ALMA-app.git
   cd ALMA-app
   pip install -r requirements.txt
   python scripts/generate_plot.py
   ```

2. Open the resulting `docs/index.html` file in a web browser to view the ALMA interface.

## Documentation

For detailed information, please refer to our [documentation](https://f-marchi.github.io/ALMA/).

## Contributing

We welcome contributions to the ALMA project! If you'd like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a new Pull Request

If you would like us to incorporate new datasets, please have them added to GEO and let us know!

## Dataset

The complete ALMA dataset is available for download [here](https://github.com/f-marchi/ALMA/raw/refs/heads/main/data/alma_main_results.xlsx). 

## License

This project is licensed under the [MIT License](LICENSE).

## Citation

TBD

## Acknowledgements

We would like to thank all contributors and supporters of the ALMA project.

---

© Copyright 2024 Marchi et al. | Lamba Lab | University of Florida
