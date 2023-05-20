import requests
from datetime import date
import pandas as pd
pd.options.display.max_columns = 999
pd.options.display.max_rows = 100
pd.options.display.width = None


api_key = '3cd55663d8b058e3c2577d5f206dc8e5'
database_path = 'database/'


def get_sports_response(api_key: str, all: bool = 'false'):
    sports_response = requests.get('https://api.the-odds-api.com/v4/sports', params={
        'api_key': api_key,
        'all': all,
    })

    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
    
    return sports_response


def get_odds_response(api_key: str, sport: str, regions: str, markets: str, odds_format: str, date_format: str):

    odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{sport}/odds', params={
        'api_key': api_key,
        'regions': regions,
        'markets': markets,
        'oddsFormat': odds_format,
        'dateFormat': date_format,
    })

    if odds_response.status_code != 200:
        raise Exception(f'The api request was not successful: status code {odds_response.status_code}, response body: {odds_response.text}')
    
    return odds_response


sports = get_sports_response(api_key=api_key, all='false')
sports_df = pd.json_normalize(data=sports.json())
today_date = date.today().strftime(format=r'%Y-%m-%d')
sports_df.to_parquet(path=database_path + f'sports_{today_date}.parquet')
print(sports_df)