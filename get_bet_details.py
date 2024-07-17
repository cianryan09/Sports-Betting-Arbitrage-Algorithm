from bf_lightweight import pd
from get_market_books import runners_df
import numpy as np
from market_catalogues import market_list
from calculate_payoffs import payoffs_total
from event_IDs import home_team, away_team

"""**Order Workflow**"""

# market_books = pd.read_csv('/content/Market_Books.csv', index_col=[0])
market_books = runners_df

# market_books[market_books['Market Name'] == 'Match Odds'].loc[:, ['Selection ID',	'Best Back Price',	'Best Back Size']]

market_books.reset_index(inplace=True)

if len(market_books) > len(market_books[market_books['Status'] == 'ACTIVE']):

    market_ids = np.concatenate([np.tile([str(m) for m in market_books[(market_books['Market Name'] == m) & (market_books['Status'] != 'ACTIVE')]['Market ID'].values] + [str(m) for m in market_books[(market_books['Market Name'] == m) & (market_books['Status'] == 'ACTIVE')]['Market ID'].values], 2) for m in market_list])

    selection_ids = np.concatenate([np.tile([str(m) for m in market_books[(market_books['Market Name'] == m) & (market_books['Status'] != 'ACTIVE')]['Selection ID'].values] + [str(m) for m in market_books[(market_books['Market Name'] == m) & (market_books['Status'] == 'ACTIVE')]['Selection ID'].values], 2) for m in market_list])

    handicaps = np.concatenate([np.tile([str(m) for m in market_books[(market_books['Market Name'] == m) & (market_books['Status'] != 'ACTIVE')]['Handicap'].values] + [str(m) for m in market_books[(market_books['Market Name'] == m) & (market_books['Status'] == 'ACTIVE')]['Handicap'].values], 2) for m in market_list])

    price = np.concatenate([np.concatenate([market_books[(market_books['Market Name'] == m) & (market_books['Status'] != 'ACTIVE')]['Best Back Price'].values, market_books[(market_books['Market Name'] == m) & (market_books['Status'] == 'ACTIVE')]['Best Back Price'].values, market_books[(market_books['Market Name'] == m) & (market_books['Status'] != 'ACTIVE')]['Best Lay Price'].values, market_books[(market_books['Market Name'] == m) & (market_books['Status'] == 'ACTIVE')]['Best Lay Price'].values]) for m in market_list])

    size = np.concatenate([np.concatenate([market_books[(market_books['Market Name'] == m) & (market_books['Status'] != 'ACTIVE')]['Best Back Size'].values, market_books[(market_books['Market Name'] == m) & (market_books['Status'] == 'ACTIVE')]['Best Back Size'].values, market_books[(market_books['Market Name'] == m) & (market_books['Status'] != 'ACTIVE')]['Best Lay Size'].values, market_books[(market_books['Market Name'] == m) & (market_books['Status'] == 'ACTIVE')]['Best Lay Size'].values]) for m in market_list])


else:

    market_ids = np.concatenate([np.tile([str(m) for m in market_books[market_books['Market Name'] == m]['Market ID'].values], 2) for m in market_list])

    selection_ids = np.concatenate([np.tile([str(m) for m in market_books[market_books['Market Name'] == m]['Selection ID'].values], 2) for m in market_list])

    handicaps = np.concatenate([np.tile([str(m) for m in market_books[market_books['Market Name'] == m]['Handicap'].values], 2) for m in market_list])

    price = np.concatenate([np.concatenate([market_books[market_books['Market Name'] == m]['Best Back Price'].values, market_books[market_books['Market Name'] == m]['Best Lay Price'].values]) for m in market_list])

    size = np.concatenate([np.concatenate([market_books[market_books['Market Name'] == m]['Best Back Size'].values, market_books[market_books['Market Name'] == m]['Best Lay Size'].values]) for m in market_list])


liability = pd.read_csv('Bet_Values.csv', index_col=[0,1,2]).to_numpy().T[0]

payoffs = payoffs_total

df_betting = pd.DataFrame({
    'Market ID': market_ids,
    'Selection ID': selection_ids,
    'Price': price,
    'Size': size,
    'Handicap': handicaps,
    'Liability': liability
    },
                          index = payoffs.index)

df_betting.reset_index(inplace = True)
df_betting['Stake'] = df_betting.apply(lambda row: np.round(row['Liability'] if row['Bet Type'] == 'Back' else (row['Price'] - 1)**(-1) * row['Liability'], 2), axis=1)

df_betting.to_csv(f'Betting_Details_{home_team}_v_{away_team}.csv')