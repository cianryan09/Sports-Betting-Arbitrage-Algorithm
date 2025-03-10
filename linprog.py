# -*- coding: utf-8 -*-
"""LinProg.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1imsK0lsIKdHyHf-tUW6ptQ-ugD8lYhds
"""

from bf_lightweight import betfairlightweight, trading, pd, np
from calculate_payoffs import payoffs_total
from get_bet_sizes import bet_size_df
from market_catalogues import market_catalogue_filtered
from get_market_books import runners_df
import pulp

# payoffs = pd.read_csv('/content/Payoffs.csv', index_col=[0,1,2], header=[0,1])
payoffs = payoffs_total
# bet_sizes = pd.read_csv('/content/Bet_Size.csv', index_col=[0,1,2])
bet_sizes = bet_size_df

# market_catalogue = pd.read_csv('/content/market_catalogue.csv', index_col=[0])
market_catalogue = market_catalogue_filtered

market_list = market_catalogue['Market Name'].values

bs_array = bet_sizes.to_numpy().T

up_bounds, low_bounds = bs_array[0], bs_array[1]

df_bounds = pd.DataFrame({'Low': low_bounds, 'High': up_bounds}, index = payoffs.index)

# df_bounds.to_csv('bounds.csv')

p = payoffs.to_numpy()

p.shape

# Get the shape of the p array
num_rows, num_cols = p.shape

# Define the problem
problem = pulp.LpProblem("Maximize_Sum_Rz", pulp.LpMaximize)

# Define the decision variables
R = [pulp.LpVariable(f'R_{i}', lowBound=low_bounds[i], upBound=up_bounds[i], cat='Continuous') for i in range(num_rows)]

# Objective function: Maximize sum(R[j] * z[i, j])
objective = pulp.lpSum([R[i] * p[i, j] for i in range(num_rows) for j in range(num_cols)  ])
# objective = pulp.lpSum([R @ z])
problem += objective

# Print the objective function
# print("Objective function:  ", objective)
loss_allowance = 0.0
# Constraints: sum(R[j] * z[i, j]) >= 0 for each row i in z
for j in range(num_cols):
    constraint = pulp.lpSum([R[i] * p[i, j] for i in range(num_rows)]) >= 0
    # print(f"Constraint for row {j}: {constraint}")
    problem += constraint

# Add the constraint that the sum of R values must equal 1000
sum_constraint = pulp.lpSum(R[j] for j in range(num_rows)) == 1000
problem += sum_constraint


# Solve the problem
# problem.solve()

# Print the status of the solution
# print(f"Status: {pulp.LpStatus[problem.status]}")

# Print the values of R
R_values = np.zeros(num_rows)
for i in range(num_rows):
    R_values[i] = R[i].varValue

# print("R array:")
# print(R_values)
# print("Objective value:", pulp.value(problem.objective))

payoffs_calc = R_values[:, None] * p

bets_df = pd.DataFrame({'Bets': [R[i].varValue for i in range(num_rows)]}, index = payoffs.index)

bet_array = [R[i].varValue for i in range(num_rows)]

bets_df = pd.DataFrame(bet_array, columns = pd.MultiIndex.from_tuples([('Bet', 'Liability')]), index = payoffs.index)

bets_df.reset_index(inplace=True)

bets_df.loc['Total', :] = bets_df.sum().values

bets_df.to_csv('Bets.csv')

payoffs_df = pd.DataFrame(payoffs_calc, index = payoffs.index, columns = payoffs.columns)

payoffs_df.loc['Total', :] = payoffs_df.sum().values

payoffs_df.to_csv('Payoffs_df.csv')

"""**Order Workflow**"""

# market_books = pd.read_csv('/content/Market_Books.csv', index_col=[0])
market_books = runners_df

market_books[market_books['Market Name'] == 'Match Odds'].loc[:, ['Selection ID',	'Best Back Price',	'Best Back Size']]

market_books.reset_index(inplace=True)

market_ids = np.concatenate([np.tile([str(m) for m in market_books[market_books['Market Name'] == m]['Market ID'].values], 2) for m in market_list])

selection_ids = np.concatenate([np.tile([str(m) for m in market_books[market_books['Market Name'] == m]['Selection ID'].values], 2) for m in market_list])

handicaps = np.concatenate([np.tile([str(m) for m in market_books[market_books['Market Name'] == m]['Handicap'].values], 2) for m in market_list])

price = np.concatenate([np.concatenate([market_books[market_books['Market Name'] == m]['Best Back Price'].values, market_books[market_books['Market Name'] == m]['Best Lay Price'].values]) for m in market_list])

size = np.concatenate([np.concatenate([market_books[market_books['Market Name'] == m]['Best Back Size'].values, market_books[market_books['Market Name'] == m]['Best Lay Size'].values]) for m in market_list])

liability = bet_array

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

df_betting.to_csv('betting.csv')

# !pip install betfairlightweight

import betfairlightweight

betting_filtered = df_betting[df_betting['Liability'] > 0].loc[:, ['Market ID', 'Stake', 'Price', 'Selection ID', 'Handicap', 'Bet Type']]

def create_instructions_filter(size_, price_, selection_id, handicap, bet_type):

  # Define a limit order filter
  limit_order_filter = betfairlightweight.filters.limit_order(
      size=str(size_),
      price=str(price_),
      persistence_type='LAPSE'
  )

  # Define an instructions filter
  instructions_filter = betfairlightweight.filters.place_instruction(
      selection_id=str(selection_id),
      handicap = handicap,
      order_type="LIMIT",
      side=bet_type.upper(),
      limit_order=limit_order_filter
  )

  return instructions_filter

instructions_filter = [(betting_filtered.iloc[n,0], create_instructions_filter(*betting_filtered.iloc[n, 1:].to_list())) for n in range(len(betting_filtered))]

def place_order(mkt_id, instructions):

  # Place the order
#   order = trading.betting.place_orders(
#       market_id= mkt_id, # The market id we obtained from before
#       customer_strategy_ref='bf_strat',
#       instructions=[instructions] # This must be a list
#   )

  # Place the order test
  order = {
      'market_id': mkt_id, # The market id we obtained from before
      'customer_strategy_ref': 'bf_strat',
      'instructions': [instructions] # This must be a list
  }

  return order

for m, i in instructions_filter:
    print(place_order(m, i))

# get current orders
# current_orders = trading.betting.list_current_orders(customer_strategy_refs=['bf_strat'])['_data']['currentOrders'][0]
# current_orders_df = pd.DataFrame(current_orders)
# current_orders_df.to_csv('current_orders.csv')
