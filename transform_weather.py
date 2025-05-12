import pandas as pd
import os


def main():
    #Path to raw NOAA csv
    RAW_PATH = "data/noaa_raw.csv"
    df = pd.read_csv(RAW_PATH)

    #Convert 'date' to datetime
    df['date'] = pd.to_datetime(df['date'])

    #Filter for key weather metrics
    keep = ['TAVG', 'PRCP', 'TMAX', 'TMIN', 'AWND', 'WSFG', 'WDF2', 'WDF5', 'WSF2', 'WSF5',
        'SNOW', 'SNWD', 'WESF', 'WESD']

    df= df[df['datatype'].isin(keep)]

    #Group by date and datatype, average multiple station values
    pivot = df.groupby(['date', 'datatype'])['value'].mean().unstack()

    #Reset index for flat datafram
    pivot = pivot.reset_index()

    #Drop na's 
    pivot = pivot.dropna()

    #Save cleaned file
    CLEANED_PATH = "data/weather_cleaned.csv"
    pivot.to_csv(CLEANED_PATH, index = False)

    print(pivot.head())

    print(f"\n Saved cleaned weather data to {CLEANED_PATH}")
    
if __name__ == "__main__":
    main()
    
    

