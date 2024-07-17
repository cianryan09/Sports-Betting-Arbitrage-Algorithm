from bf_lightweight import betfairlightweight, trading
from get_bet_details import df_betting

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

def place_order(trading, mkt_id, instructions):

  # Place the order
  order = trading.betting.place_orders(
      market_id= mkt_id, # The market id we obtained from before
      customer_strategy_ref='bf_strat',
      instructions=[instructions] # This must be a list
  )

  # Place the order test
#   order = {
#       'market_id': mkt_id, # The market id we obtained from before
#       'customer_strategy_ref': 'bf_strat',
#       'instructions': [instructions] # This must be a list
#   }

  return order

for m, i in instructions_filter:
    print(place_order(trading, m, i))