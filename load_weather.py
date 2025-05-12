import sqlite3
import pandas as pd
import os

def main():
    #Path the cleaned csv
    CLEANED_PATH = "data/weather_cleaned.csv"
    DB_PATH = "weather.db"

    #read cleaned data
    df = pd.read_csv(CLEANED_PATH)

    #Connect to SQLITE DV
    conn = sqlite3.connect(DB_PATH)

    #Load into DB- replaces table if it exists
    df.to_sql("daily_weather", conn,  if_exists="replace", index=False)

    #confirm write 
    print(f"\n Loaded {len(df)} rows into 'daily_weather' table in {DB_PATH}")

    #Preview top 5 rows
    preview=pd.read_sql("SELECT * FROM daily_weather LIMIT 5;", conn)
    print(preview)

    #Close connection
    conn.close()

if __name__ == "__main__":
    main()
    