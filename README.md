NOAA Weather ETL Pipeline
Project Overview
This project implements a full ETL (Extract, Transform, Load) pipeline using Python and Prefect to collect, clean, and store historical daily weather data for Boston, Massachusetts from 2019 to 2024.

Data Source
Provider: NOAA Climate Data Online (CDO) API

Dataset: Global Historical Climatology Network - Daily (GHCND)

Location: Boston (CITY:US250002)

Pipeline Structure
Extract
Collects daily weather observations from NOAA in yearly chunks.

Automatically paginates using the API’s offset parameter.

Handles server issues using exponential backoff retry logic.

Saves raw data to: data/noaa_raw.csv

Transform
Filters for key weather variables:

Temperature (TAVG, TMIN, TMAX)

Precipitation (PRCP, SNOW, SNWD)

Wind (AWND, WSF2, WSF5)

Aggregates across stations to daily averages.

Drops rows with missing values.

Saves cleaned data to: data/weather_cleaned.csv

Load
Loads the transformed dataset into a local SQLite database: weather.db

Table name: daily_weather

Automation with Prefect
Pipeline orchestrated using Prefect

Tasks (extract, transform, load) defined as Prefect tasks and run within a flow.

Run the entire pipeline with:

bash
Copy
Edit
python weather_pipeline.py
Project Files
extract_weather.py: Extracts and saves raw NOAA weather data

transform_weather.py: Cleans and reshapes raw data into structured format

load_weather.py: Loads cleaned data into SQLite

weather_pipeline.py: Prefect ETL flow coordinating the full pipeline

.env: Contains NOAA API token (not tracked by Git)

requirements.txt: Python dependencies

Getting Started
Clone this repo

Set up a virtual environment and install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Add your NOAA API token to a .env file:

ini
Copy
Edit
NOAA_TOKEN=your_token_here
Run the full ETL pipeline:

bash
Copy
Edit
python weather_pipeline.py
