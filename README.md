# NOAA Weather ETL Pipeline

## Project Overview
This project implements a full ETL (Extract, Transform, Load) pipeline using Python and Prefect to collect, clean, and store historical daily weather data for Boston, Massachusetts from 2019 to 2024.

## Data Source
- **Provider**: NOAA Climate Data Online (CDO) API  
- **Dataset**: Global Historical Climatology Network - Daily (GHCND)  
- **Location**: Boston (`CITY:US250002`)

## Pipeline Structure

### Extract
- Collects daily weather observations from NOAA in yearly chunks.
- Automatically paginates using the API’s `offset` parameter.
- Handles server issues using exponential backoff retry logic.
- Saves raw data to: `data/noaa_raw.csv`

### Transform
- Filters for key weather variables:
  - Temperature (`TAVG`, `TMIN`, `TMAX`)
  - Precipitation (`PRCP`, `SNOW`, `SNWD`)
  - Wind (`AWND`, `WSF2`, `WSF5`)
- Aggregates across stations to daily averages.
- Drops rows with missing values.
- Saves cleaned data to: `data/weather_cleaned.csv`

### Load
- Loads the transformed dataset into a local SQLite database: `weather.db`
- Table name: `daily_weather`

## Automation with Prefect
- Pipeline orchestrated using **Prefect**
- Tasks (`extract`, `transform`, `load`) defined as Prefect tasks and run within a flow.
- Run the entire pipeline with:
  ```bash
  python weather_pipeline.py
