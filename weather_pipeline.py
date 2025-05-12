from prefect import flow, task
import extract_weather
import transform_weather
import load_weather

@task
def extract():
    extract_weather.main()
    
@task
def transform():
    transform_weather.main()
    
@task
def load():
    load_weather.main()
    
@flow
def weather_etl_flow():
    extract()
    transform()
    load()
    
if __name__ == "__main__":
    weather_etl_flow()

