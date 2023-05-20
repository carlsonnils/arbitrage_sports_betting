import requests
import pandas as pd
import json


#    get the api key from a .txt file
def load_api_key(key_path: str):
    with open(key_path, mode='r') as file:
        API_KEY = file.read()
    return API_KEY


#   Get Sports info on in season sports
def get_sports_data_df(api_key: str, return_data: bool = False, return_headers: bool = False):

    sports_response = requests.get('https://api.the-odds-api.com/v4/sports', params={
        'api_key': api_key
    })

    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
    else:
        # write sports data to database in "in_season_sports" table
        df = pd.DataFrame(sports_response.json())
        # write headers info to database in "in_season_sports_headers" table
        headers = sports_response.headers
        headers_df = pd.DataFrame(data=dict(headers), index=[0])
    
    if return_data:
        return df
    if return_headers:
        return headers_df
    
    return df, headers_df


def get_sports_response(api_key: str):
    sports_response = requests.get('https://api.the-odds-api.com/v4/sports', params={
        'api_key': api_key
    })

    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
    
    return sports_response


def get_odds_data_df(api_key: str, sport: str, regions: str, markets: str, odds_format: str, date_format: str):

    odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{sport}/odds', params={
        'api_key': api_key,
        'regions': regions,
        'markets': markets,
        'oddsFormat': odds_format,
        'dateFormat': date_format,
    })

    if odds_response.status_code != 200:
        raise Exception(f'The api request was not successful: status code {odds_response.status_code}, response body: {odds_response.text}')

    # json_file_path = r'/home/carls/projects/odds_site/odds_site_db/epl_odds_response.json'
    # with open(json_file_path, mode='w') as json_file:
    #     odds_json = json.dump(odds_response.json(), json_file)

    extra_meta = [
        ['bookmakers', 'key'], 
        ['bookmakers', 'title'], 
        ['bookmakers', 'last_update'], 
        ['bookmakers', 'markets', 'last_update'], 
        ['bookmakers', 'markets', 'key']
    ]
    meta = pd.json_normalize(data=odds_response.json()).columns.to_list()[:-1] + extra_meta

    odds_df = pd.json_normalize(
        data=odds_response.json(),
        meta=meta,
        record_path=['bookmakers', 'markets', 'outcomes'],
    )

    odds_headers_df = pd.DataFrame(dict(odds_response.headers), index=[0])

    return odds_df, odds_headers_df


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

