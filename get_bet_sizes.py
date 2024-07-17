from bf_lightweight import pd, np
from get_market_books import runners_df
from calculate_payoffs import payoffs_total
from market_catalogues import market_list

def bet_size(runners_df, market_):

    back_size = runners_df[runners_df['Market Name'] == market_]['Best Back Size'].values
    lay_price = runners_df[runners_df['Market Name'] == market_]['Best Lay Price'].values - 1
    lay_size = np.round(runners_df[runners_df['Market Name'] == market_]['Best Lay Size'].values * lay_price, 2)

    size_array = np.concatenate([back_size, lay_size])

    return size_array


max_size = np.concatenate([bet_size(runners_df, market) for market in market_list])
min_size = np.zeros(len(max_size))

bet_size_df = pd.DataFrame({'Max Size': max_size, 'Min Size': min_size}, index = payoffs_total.index)

bet_size_df.to_csv('Bet_Size.csv')