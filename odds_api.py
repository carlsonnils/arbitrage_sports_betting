import requests


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


def get_sports_response(api_key: str, all_sports: bool = 'false'):

    sports_response = requests.get('https://api.the-odds-api.com/v4/sports', params={
        'api_key': api_key,
        'all': all_sports,
    })

    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
    
    return sports_response