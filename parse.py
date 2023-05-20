from datetime import date
import pandas as pd
pd.options.display.max_columns = 999
pd.options.display.max_rows = 100
pd.options.display.width = None


api_key = '3cd55663d8b058e3c2577d5f206dc8e5'
database_path = 'database/'
today_date = date.today().strftime(format=r'%Y-%m-%d')


###########################
#
#   SPORTS
#
###########################

def load_active_sports(sports_response):

    sports_df = pd.json_normalize(data=sports_response.json())
    sports_headers_df = pd.DataFrame(dict(sports_response.headers), index=[0])

    sports_path = database_path + f'sports_{today_date}'
    sports_df.to_parquet(path=sports_path + '.parquet', index=False)
    sports_df.to_csv(sports_path + '.csv', index=False)

    sports_headers_path = database_path + f'sports_headers_{today_date}'
    sports_headers_df.to_parquet(path=sports_headers_path + '.parquet', index=False)
    sports_headers_df.to_csv(sports_headers_path + '.csv', index=False)    

    return sports_df


###########################
#
#   ODDS
#
###########################

def to_dt(srs):
        srs = pd.to_datetime(srs, utc=True).dt.tz_convert(tz='US/Eastern').dt.tz_localize(tz=None)
        return srs


# sport_key = 'baseball_mlb'
# sregion = 'us'
# market = 'h2h'
# odds_format = 'decimal'
# date_format = 'iso'

# odds_response = get_odds_response(api_key=api_key, sport=sport_key, regions=region, markets=market, odds_format=odds_format, date_format=date_format)
# odds_headers_df = pd.DataFrame(dict(odds_response.headers), index=[0])
# odds_headers_path = database_path + f'odds_headers_{today_date}.csv'
# odds_headers_df.to_csv(odds_headers_path)


def format_for_arbitrage(json_data):

    df = pd.json_normalize(
        json_data, 
        record_path=['bookmakers', 'markets', 'outcomes'],
        meta=[
            'id',
            'commence_time',
            'sport_title',
            'home_team',
            'away_team',
            ['bookmakers', 'key'],
            ['bookmakers', 'markets', 'last_update']
        ]
    )

    col_rename = {
            'id': 'ID',
            'commence_time': 'Start_Time',
            'name': 'Team',
            'price': 'Line',
            'sport_title': 'League',
            'home_team': 'Home_Team',
            'away_team': 'Away_Team',
            'bookmakers.key': 'Book',
            'bookmakers.markets.last_update': 'Line_Update'
    }

    df = df.rename(columns=col_rename)
    df['Start_Time']  = to_dt(df['Start_Time'])
    df['Line_Update'] = to_dt(df['Line_Update'])

    game_ids = df['ID'].drop_duplicates().reset_index(drop=True)
    game_map = dict(zip(game_ids.values, game_ids.index))
    df['Game_ID'] = df['ID'].map(game_map)

    df = df[[
        'ID',
        'Game_ID',
        'Team',
        'Line',
        'Book',
        'Home_Team',
        'Away_Team',
        'Start_Time',
        'League',
        'Line_Update',
    ]]

    df = (
    df.convert_dtypes(infer_objects=True)
        .astype(dtype={'Game_ID': 'string'})
    )

    return df


# odds_df = format_for_arbitrage(odds_response.json())
# odds_path = database_path + f'odds_{today_date}'
# odds_df.to_parquet(path=odds_path + '.parquet', index=False)
# odds_df.to_csv(odds_path + '.csv', index=False)
# print(odds_df, odds_headers_df)

def load_odds_data(response):
    df = format_for_arbitrage(response.json())

    path = database_path + f'odds_{today_date}'
    df.to_parquet(path=path + '.parquet', index=False)
    df.to_csv(path + '.csv', index=False)

    return df

