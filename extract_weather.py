import requests
import pandas as pd
import os
from dotenv import load_dotenv
import time
import requests

def main():
    #Load .env
    load_dotenv()
    TOKEN = os.getenv("NOAA_TOKEN")

    #NOAA endpoint and headers
    BASE_URL = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
    HEADERS = {"token": TOKEN}

    #create list of start, end ranges
    date_ranges = [
        ("2019-05-01", "2020-04-30"),
        ("2020-05-01", "2021-04-30"),
        ("2021-05-01", "2022-04-30"),
        ("2022-05-01", "2023-04-30"),
        ("2023-05-01", "2024-04-30")
    ]

    #Expanded datatypes of interest (can be filtered later)
    requested_datatypes = [
        "TAVG", "TMAX", "TMIN",  # temperature
        "PRCP", "SNOW", "SNWD",  # precipitation/snow
        "AWND", "WSF2", "WSF5",  # wind
        "WT01", "WT03", "WT04", "WT05", "WT06", "WT08", "WT09"  # weather types
    ]

    #Initialize results
    all_results = []

    MAX_RETRIES = 5
    #Define request parameters
    for start, end in date_ranges:
        print(f"\n Fetching data from {start} to {end}")
        offset = 1
        while True:
            retries = 0
            while retries < MAX_RETRIES:
                params = {
                    "datasetid": "GHCND",
                    "locationid": "CITY:US250002",
                    "startdate": start,
                    "enddate": end,
                    "limit": 1000,
                    "offset": offset,
                    "units": "standard",
                    "datatypeid": requested_datatypes,
                }

                response = requests.get(BASE_URL, headers=HEADERS, params=params)
                if response.status_code == 200:
                    break
                elif response.status_code == 503:
                    print(f"503 error. Retrying in {2 ** retries} seconds...")
                    time.sleep(2 ** retries)
                    retries += 1
                else:
                    print(f"Request failed with {response.status_code}")
                    print(response.text)
                    break

            if retries == MAX_RETRIES:
                print("Max retries exceeded. Moving to next range.")
                break

            data = response.json()
            results = data.get("results", [])
            if not results:
                break

            all_results.extend(results)
            print(f"Fetched {len(results)} records (total: {len(all_results)})")
            offset += 1000
            time.sleep(1)


    #Convert to df
    df = pd.DataFrame(all_results)

    #Preview
    print(df.head())

    # Save to /data/ directory
    os.makedirs("data", exist_ok=True)
    RAW_PATH = "data/noaa_raw.csv"
    df.to_csv(RAW_PATH, index=False)


    print(f"\n Extracted and saved {len(df)} rows to {RAW_PATH}")

if __name__ == "__main":
    main()