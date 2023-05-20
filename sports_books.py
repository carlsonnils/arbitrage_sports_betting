import pandas as pd


ny_books = pd.read_csv('database/odds_api_ny_bookmakers.csv')
nybooks_list = ny_books['Bookmaker_key'].to_list()
with open('database/ny_books.py', mode='w') as nybooks_file:
    nybooks_file.write('ny_books = [')
    for book in nybooks_list:
        nybooks_file.write(f"\n\t'{book}',")
    nybooks_file.write('\n]')
print(ny_books)