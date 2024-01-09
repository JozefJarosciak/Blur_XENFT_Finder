# XENFT Finder for Blur.io

## Description
XENFT Finder is a Python script designed to help users programmatically find the best XENFTs on the Blur.io website. It automates the process of fetching data from Blur.io and analyzing XENFTs based on various metrics. The script sorts the XENFTs based on configurable criteria, providing a clear and organized table of results.

## Features
- Fetches XENFT data directly from Blur.io.
- Calculates key metrics for each XENFT.
- Sorts XENFTs based on user-defined criteria.
- Presents data in an easy-to-read table format.

## Screenshot
![image](https://github.com/JozefJarosciak/Blur_XENFT_Finder/assets/3492464/dc76476f-8601-49a5-abbe-eb00b57d2da4)

## Configurable Options
This script offers several configurable options to tailor its functionality to your needs:
- `ETH_TO_USD`: Set to `False` to use a fixed ETH to USD conversion rate. Default is `True`.
- `XEN_TO_USD`: Set to `False` to use a fixed XEN to USD conversion rate. Default is `True`.
- `ETH_USD_FIXED`: Fixed ETH to USD rate if `ETH_TO_USD` is `False`. Default is `2300`.
- `XEN_USD_FIXED`: Fixed XEN to USD rate if `XEN_TO_USD` is `False`. Default is `0.00000038`.
- `XEN_GLOBAL_RANK`: Approximate global rank of XEN. Default is `19_960_000`.
- `TERM_MIN`: Minimum term length for considered XENFTs. Default is `100`.
- `VMU_MIN`: Minimum VMU value for considered XENFTs. Default is `10`.
- `SORT_BY`: Criterion for sorting XENFTs. This determines the primary attribute used to order the fetched XENFTs. The options are:
  - `"xen_per_usd"`: Sorts XENFTs based on the amount of XEN you get per USD. This metric is useful for identifying XENFTs that potentially offer more XEN for a lower price.
  - `"price_per_vmu_usd"`: Sorts XENFTs based on their price per VMU (Virtual Machine Unit) in USD. This can help find XENFTs that are relatively cheaper in terms of their computational power.
  - `"ratio"`: Sorts XENFTs based on the ratio of the XEN value in USD to the price in USD. A higher ratio indicates a potentially more valuable XENFT relative to its cost. This is the default sorting criterion.
- `CLASS_VALUES`: Array of XENFT classes to be considered.
- `MATURITY_YEARS`: Array of maturity years to be considered.

## Installation
To run the XENFT Finder script, you need Python installed on your system, along with a few additional libraries. Follow these steps to set up the environment:

1. **Install Python**: If you don't have Python installed, download and install it from [python.org](https://www.python.org/downloads/). This script should be compatible with Python 3.6 and later (tested on 3.11)
2. **Install Dependencies**:
   - Ensure you are in the project directory where the `requirements.txt` file is located.
   - Run `pip install -r requirements.txt` to install the required Python libraries.

## Usage
After installation, you can run the script from the terminal or command prompt. Here’s how to use it:

1. Navigate to the project directory.

2. Run the script using Python:
   ```sh
   python xenft_finder.py
