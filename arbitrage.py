from datetime import date
import pandas as pd
from database import ny_books

database_path = 'database/'
sport_title = 'MLB'
ny_books_list = ny_books.list


def calculate_arbitrage(df, save: bool = True):
    df['WinProbability'] = 1 / df.Line

    games = df.Game_ID.drop_duplicates().to_list()
    odds_combinations = []
    for game in games:
        game_df = df.query("Game_ID == @game")
        books = game_df.Book.drop_duplicates().to_list()

        for book in books:
            book_df = game_df.query("Book == @book").copy()
            otherbook_df = game_df.query("Book != @book").copy()
            teams = book_df.Team.drop_duplicates().to_list()

            for team in teams:
                team_info = book_df.query("Team == @team").copy()
                opp_info = otherbook_df.query("Team != @team").copy()
                team_line = team_info['Line'].to_list()[0]
                opp_info['BookB'] = book
                opp_info['TeamB'] = team
                opp_info['LineB'] = team_line
                opp_info['WinProbabilityB'] = team_info['WinProbability'].to_list()[0]
                opp_info['CombineWinProbability'] = opp_info['WinProbability'] + opp_info['WinProbabilityB']
                opp_info['WagerB'] = 100
                team_winpayout = 100 * team_line
                opp_info['PayoutB'] = team_winpayout
                opp_info['WagerA'] = team_winpayout / opp_info['Line']
                opp_info['PayoutA'] = opp_info['WagerA'] * opp_info['Line']
                opp_info['CombineWager'] = opp_info['WagerA'] + opp_info['WagerB']
                opp_info['CombinePayuot'] = opp_info['PayoutA'] + opp_info['PayoutB']
                opp_info['MinimumNetPayout'] = (opp_info['PayoutA'] - opp_info['CombineWager']).clip(upper=(team_winpayout - opp_info['CombineWager']))
                opp_info['MaximumNetPayout'] = (team_winpayout - opp_info['CombineWager']).clip(upper=(opp_info['PayoutA'] - opp_info['CombineWager']))
                opp_info['WagerARounded'] = opp_info['WagerA'].round(decimals=0)
                opp_info['PayoutARounded'] = opp_info['WagerARounded'] * opp_info['Line']
                opp_info['CombineWagerRounded'] = opp_info['WagerARounded'] + opp_info['WagerB']
                opp_info['CombinePayuotRounded'] = opp_info['PayoutARounded'] + opp_info['PayoutB']
                opp_info['MinimumNetPayoutRounded'] = (opp_info['PayoutARounded'] - opp_info['CombineWagerRounded']).clip(upper=(team_winpayout - opp_info['CombineWagerRounded']))
                opp_info['MaximumNetPayoutRounded'] = (team_winpayout - opp_info['CombineWagerRounded']).clip(upper=(opp_info['PayoutARounded'] - opp_info['CombineWagerRounded']))
                odds_combinations.append(opp_info)
    
    all_combinations_df = (
        pd
        .concat(odds_combinations, axis=0)
        .sort_values(by=['Game_ID', 'Book', 'Team'])
        .reset_index(drop=True)
    )

    if save:
        today_date = date.today().strftime(format=r'%Y-%m-%d')
        arbitrage_mlb_path = database_path + f'arbitrage_{sport_title}_{today_date}'
        all_combinations_df.to_parquet(arbitrage_mlb_path + '.parquet', index=False)
        all_combinations_df.to_csv(arbitrage_mlb_path + '.csv', index=False)
    
    return all_combinations_df


###########################
#
#   ALL BOOKS
#
###########################

# all_combinations_df = (
#     pd
#     .concat(odds_combinations, axis=0)
#     .sort_values(by=['Game_ID', 'Book', 'Team'])
#     .reset_index(drop=True)
# )
# today_date = date.today().strftime(format=r'%Y-%m-%d')
# arbitrage_mlb_path = database_path + f'arbitrage_{sport_title}_{today_date}'
# all_combinations_df.to_parquet(arbitrage_mlb_path + '.parquet', index=False)
# all_combinations_df.to_csv(arbitrage_mlb_path + '.csv', index=False)


###########################
#
#   NY BOOKS
#
###########################

# ny_combinations_df = (
#     all_combinations_df
#     .query("(Book == @ny_books_list) & (BookB == @ny_books_list)")
#     .sort_values(by=['MinimumNetPayout'], ascending=False)
# )
# arbitrage_mlb_ny_path = database_path + f'arbitrage_{sport_title}_ny_{today_date}'
# ny_combinations_df.to_parquet(arbitrage_mlb_ny_path + '.parquet', index=False)
# ny_combinations_df.to_csv(arbitrage_mlb_ny_path + '.csv', index=False)
