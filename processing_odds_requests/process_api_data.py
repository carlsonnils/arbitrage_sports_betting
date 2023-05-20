import json
from datetime import datetime
import pandas as pd
pd.set_option('display.max_columns', 100)
pd.options.display.width = 0


def to_dt(srs):
        srs = pd.to_datetime(srs, utc=True).dt.tz_convert(tz='US/Eastern').dt.tz_localize(tz=None)
        return srs


json_path = r'/home/carls/projects/odds_site/processing_odds_requests/first_ever_request.json'
with open(json_path,'r') as f:
        data = json.loads(f.read())

df = pd.json_normalize(
    data, 
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
        'commence_time': 'Start Time',
        'name': 'Team',
        'price': 'Line',
        'sport_title': 'League',
        'home_team': 'Home Team',
        'away_team': 'Away Team',
        'bookmakers.key': 'Book',
        'bookmakers.markets.last_update': 'Line Update'
}

df = df.rename(columns=col_rename)

df['Start Time']  = to_dt(df['Start Time'])
df['Line Update'] = to_dt(df['Line Update'])

game_ids = df['ID'].drop_duplicates().reset_index(drop=True)
game_map = dict(zip(game_ids.values, game_ids.index))
df['Game ID'] = df['ID'].map(game_map)

df = df[[
    'ID',
    'Game ID',
    'Team',
    'Line',
    'Book',
    'Home Team',
    'Away Team',
    'Start Time',
    'League',
    'Line Update',
]]

# set the correct data types
df = (
    df.convert_dtypes(infer_objects=True)
    .astype(dtype={'Game ID': 'string'})
)

print(df)

# df.to_parquet(path='first_odds_req.parquet')


