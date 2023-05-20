import pandas as pd
pd.set_option('display.max_columns', 100)
pd.options.display.width = 150
import numpy as np
import time


def calc_payout(odds: float, wager: float) -> float:
    return odds * wager


def calc_prob(line1: float, line2: float) -> float:
    win_prob = (1 / line1) + (1 / line2)
    return win_prob


def check_odds_format(odds, odds_format: str) -> bool:
    if isinstance(odds, float):
        return True
    return False


def get_fav_and_dog(lines: list) -> tuple:
    fav = min(lines)
    ud = max(lines)
    return fav, ud


def get_unique_vals(df: pd.DataFrame, column: str | int):
    if isinstance(column, str):
        return df[column].drop_duplicates().tolist()
    if isinstance(column, int):
        return df.iloc[:, column].drop_duplicates().tolist()


def calc_arbitrage(
        game_info: pd.DataFrame,
        round_wagers: bool = True,
        dog_wager: int = 20,
        odds_format: str = 'decimal',
        odd_col: str | int = 'Line',
        team_col: str | int = 'Team',
    ) -> pd.DataFrame:

    if odds_format.lower() != 'decimal':
        return print('MUST INPUT ODDS/LINE IN DECIMAL FORMAT')

    odds = get_unique_vals(game_info, odd_col)
    fav_odds, dog_odds = get_fav_and_dog(odds)

    win_prob = calc_prob(fav_odds, dog_odds)
    if win_prob <= 1:
        print(f'cannot win, probability = {win_prob:.2%}')
    
    dog_po = dog_odds * dog_wager
    fav_wager = dog_po / fav_odds
    if round_wagers:
        fav_wager = np.round(fav_wager, 0)
    fav_po = fav_wager * fav_odds
    
    arbi = game_info.copy()
    arbi.loc[arbi[odd_col] == dog_odds, 'Wager'] = dog_wager
    arbi.loc[arbi[odd_col] == fav_odds, 'Wager'] = fav_wager
    arbi.loc[arbi[odd_col] == dog_odds, 'Payout'] = dog_po
    arbi.loc[arbi[odd_col] == fav_odds, 'Payout'] = fav_po
    arbi.loc[arbi[odd_col] == dog_odds, 'Net Payout'] = dog_po - fav_wager
    arbi.loc[arbi[odd_col] == fav_odds, 'Net Payout'] = fav_po - dog_wager
    arbi.loc[arbi[odd_col] == dog_odds, 'Win Probability'] = 1 / dog_odds
    arbi.loc[arbi[odd_col] == fav_odds, 'Win Probability'] = 1 / fav_odds
    arbi.loc[:, 'Total Probability'] = win_prob

    return arbi


def process_odds():
    # time the meat of the script
    t0 = time.time_ns()

    # read the dataframe in
    df_path = r'processing_odds_requests/first_odds_req.parquet'
    df = pd.read_parquet(path=df_path)

    # # create a game id
    # team_id = dict(zip(df['Team'].drop_duplicates().reset_index(drop=True).values, df['Team'].drop_duplicates().reset_index(drop=True).index.astype(str)))
    # df.insert(loc=1, column='Team ID', value=df['Game ID'] + df['Team'].map(team_id))

    for game in df['Game ID'].drop_duplicates().values:
        game_df = df[df['Game ID'] == game]
        
        teams = game_df['Team'].drop_duplicates().tolist()
        if len(teams) > 2:
            continue
        team1, team2 = teams
        
        team1_odds = game_df.loc[game_df['Team'] == team1, 'Line'].max()
        team2_odds = game_df.loc[game_df['Team'] == team2, 'Line'].max()

        team_info = game_df.loc[
            (game_df['Line'] == team1_odds) | (game_df['Line'] == team2_odds),
            ['Game ID', 'Team', 'Line', 'Book']
        ].reset_index(drop=True)

        print(team_info)

        print(calc_arbitrage(team_info))


    # time the meat of the script
    t1 = time.time_ns()
    time_ms = (t1 - t0) / (10 ** 6)
    print(f'\n{time_ms} ms')

