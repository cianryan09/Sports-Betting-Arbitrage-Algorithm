from linprog2 import R_values
from bf_lightweight import pd
from calculate_payoffs import payoffs_total
from event_IDs import home_team, away_team

payoffs = payoffs_total

payoffs_calc = R_values[:, None] * payoffs.to_numpy()

payoffs_df = pd.DataFrame(payoffs_calc, index = payoffs.index, columns = payoffs.columns)

payoffs_df.loc['Total', :] = payoffs_df.sum().values

csv_filename = f'Payoffs_df2_{home_team}_v_{away_team}.csv'
payoffs_df.to_csv(csv_filename)