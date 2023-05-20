from datetime import date
import odds_api
import parse
import arbitrage
from database import ny_books


ny_books_list = ny_books.list


if __name__ == '__main__':

    API_KEY='3cd55663d8b058e3c2577d5f206dc8e5'

    sports_res = odds_api.get_sports_response(api_key=API_KEY)
    sports_df = parse.load_active_sports(sports_response=sports_res)
    
    SPORT_KEY='baseball_mlb'
    REGION='us'
    MARKET='h2h'
    ODDS_FORMAT='decimal'
    DATE_FORMAT='iso'

    odds_res = odds_api.get_odds_response(api_key=API_KEY, sport=SPORT_KEY, regions=REGION, markets=MARKET, odds_format=ODDS_FORMAT, date_format=DATE_FORMAT)
    odds_df = parse.load_odds_data(odds_res)
    arbi_df = arbitrage.calculate_arbitrage(odds_df)

    print(odds_df, arbi_df)

    ###########################
    #
    #   NY BOOKS
    #
    ###########################

    today_date = date.today().strftime(format=r'%Y-%m-%d')

    ny_arbi_df = (
        arbi_df
        .query("(Book == @ny_books_list) & (BookB == @ny_books_list)")
        .sort_values(by=['MinimumNetPayout'], ascending=False)
    )
    arbitrage_mlb_ny_path = f'database/arbitrage_MLB_ny_{today_date}'
    ny_arbi_df.to_parquet(arbitrage_mlb_ny_path + '.parquet', index=False)
    ny_arbi_df.to_csv(arbitrage_mlb_ny_path + '.csv', index=False)