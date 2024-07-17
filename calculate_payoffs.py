from bf_lightweight import pd, np
from get_market_books import runners_df
from read_outcome_table import outcome_df
from market_catalogues import market_list
# import numpy as np

def payoffs(market, outcome_df, runners_df):

    match_odds_back = outcome_df.loc[pd.IndexSlice[market, :, 'Back'], :].to_numpy()

    match_odds_lay = outcome_df.loc[pd.IndexSlice[market, :, 'Lay'], :].to_numpy()

    prices_back = runners_df[runners_df['Market Name'] == market]['Best Back Price'].values

    prices_lay = runners_df[runners_df['Market Name'] == market]['Best Lay Price'].values

    # payments_back = np.array([[price if n == True or n == 'True' else -1 if n == False or n == 'False' else 1 if n == 'VOID' else 0.5 for n in market_array] for price,market_array in zip(prices_back, match_odds_back)])
    payments_back = np.array([[(price - 1) * 0.95 if n == True or n == 'True' else -1 if n == False or n == 'False' else 0 if n == 'VOID' else 0.5 * (price - 1) * 0.95 if n == 'HALF WIN' else -0.5 if n == 'HALF LOSE' else 0 for n in market_array] for price,market_array in zip(prices_back, match_odds_back)])
    # payments_lay = np.array([[1 + (price - 1) ** (-1) if n == True or n == 'True' else -1 if n == False or n == 'False' else 1 if n == 'VOID' else 0.5 for n in market_array] for price,market_array in zip(prices_lay, match_odds_lay)])
    payments_lay = np.array([[((price - 1) ** (-1))* 0.95 if n == True or n == 'True' else -1 if n == False or n == 'False' else 0 if n == 'VOID' else 0.5 * ((price - 1) ** (-1))*0.95 if n =='HALF WIN' else -0.5 if n == 'HALF LOSE' else 0 for n in market_array] for price,market_array in zip(prices_lay, match_odds_lay)])
    payoffs = np.vstack([payments_back, payments_lay])

    # payoffs_df = pd.DataFrame(payoffs, columns= outcome_df.columns,  index = outcome_df.loc[pd.IndexSlice[market, :, :], :].index)
    return payoffs

# payoffs_total = pd.concat([payoffs(m, outcome_df, runners_df) for m in market_list])

payoffs_total = pd.DataFrame(np.vstack([payoffs(m, outcome_df, runners_df) for m in market_list]), columns= outcome_df.columns,  index = outcome_df.loc[pd.IndexSlice[market_list, :, :], :].index)

payoffs_total.to_csv('Payoffs.csv')

print(payoffs_total.loc[:, pd.IndexSlice[(range(9+1)), (range(9+1))]].columns)
