# Cuba, New Mexico – Transportation Analysis

## Streamlit Application

**View the interactive application:** [Cuba Transportation Dashboard](https://group17-eng220-holdenjustus.streamlit.app/)

## Overview

This folder contains an independent data analysis examining transportation patterns and household vehicle availability in Cuba, New Mexico.

The analysis uses data from the U.S. Census Bureau's American Community Survey (ACS) 2024 five-year estimates. MATLAB was used to process the selected datasets and generate CSV files, which are then used by a Streamlit application to create data visualizations.

The purpose of this analysis is to examine how residents commute, how long workers spend traveling to work, and the availability of vehicles within households.

## Research Areas

This analysis focuses on three transportation-related topics:

### 1. Transportation Methods (ACS B08006)

Examines how workers travel to their jobs, including:

- Driving alone
- Carpooling
- Walking
- Public transportation
- Working from home
- Other transportation methods

### 2. Travel Time to Work (ACS B08303)

Examines the amount of time workers spend commuting to their jobs. This includes different commute-time ranges, from less than five minutes to 90 minutes or longer.

### 3. Vehicles Available per Household (ACS B08201)

Examines the number of vehicles available to households, including households with no vehicle access and those with one or multiple vehicles.

Together, these three areas provide complementary perspectives on transportation patterns and access to personal transportation in Cuba, New Mexico.

## Folder Contents

| File | Purpose |
|---|---|
| `cuba_transport.m` | MATLAB script for processing the selected ACS datasets. |
| `app.py` | Streamlit application that displays the transportation visualizations. |
| `modes.csv` | Processed transportation methods data (B08006). |
| `time.csv` | Processed commute-time data (B08303). |
| `vehicles.csv` | Processed household vehicle availability data (B08201). |
| `requirements.txt` | Python packages required to run the Streamlit application. |

## Technologies and Data Sources

- **MATLAB:** Processing and organizing Census data.
- **Python:** Application development and data handling.
- **Streamlit:** Interactive application and data visualization.
- **Pandas:** Reading and organizing CSV datasets.
- **Altair:** Creating data visualizations.
- **U.S. Census Bureau:** American Community Survey 2024 five-year estimates.

## Running the Application

The Streamlit application reads the three processed CSV files from the same directory as `app.py`.

To run the application locally:

1. Install Python.
2. Open a terminal in this folder.
3. Install the required packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python -m streamlit run app.py
   ```

The application should open in a web browser.

## Data Limitations

The American Community Survey provides estimates rather than exact population counts. These estimates include margins of error, which are particularly important when examining smaller communities.

The results should therefore be interpreted with consideration for their sample sizes and statistical reliability.

Additionally, these datasets describe commuting methods, commute durations, and household vehicle availability. They do not directly measure road conditions, vehicle reliability, fuel availability, or access to specific services.

## Scope of This Analysis

This folder documents the transportation datasets, MATLAB processing, CSV outputs, and Streamlit visualizations developed for this analysis.

It is intended to serve as a standalone record of the data-processing methods, selected research areas, and resulting visualizations.
