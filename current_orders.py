from bf_lightweight import trading, pd, np
from read_outcome_table import outcome_df as out_df, home_team, away_team
from get_market_books import runners_df

# get current orders
current_orders = trading.betting.list_current_orders(customer_strategy_refs=['bf_strat'])['_data']['currentOrders']
current_orders_df = pd.json_normalize(current_orders)
# current_orders_df = pd.read_csv('current_orders.csv', dtype={'marketId': str, 'selectionId': str})

if not current_orders_df.empty:
    current_orders_df.columns = current_orders_df.columns.str.replace('priceSize.', '')
    
    # current_orders_df = pd.read_csv('current_orders.csv', dtype = {'marketId': str, 'selectionId': str})

    bet_details = runners_df
    # bet_details = pd.read_csv('Market_Books.csv', dtype={'Market ID': str, 'Selection ID': str})
    bet_details.reset_index(inplace=True)
 

    current_orders_back = current_orders_df[(current_orders_df['side'] == 'BACK') & (current_orders_df['status'] == 'EXECUTION_COMPLETE')].loc[:, ['marketId', 'selectionId', 'handicap']].to_numpy()

    if current_orders_back.size !=0:
        selections_back = pd.concat([bet_details[(bet_details['Market ID'] == m) & (bet_details['Selection ID'] == s) & (bet_details['Handicap'] == h)].loc[:, ['Market Name', 'Selection Name']] for m,s,h in current_orders_back])
        out_idx_back = [(a,b,'Back') for (a,b) in list(selections_back.itertuples(index=False, name=None))]
        price_size_back = current_orders_df[(current_orders_df['side'] == 'BACK') & (current_orders_df['status'] == 'EXECUTION_COMPLETE')][['price', 'size']].to_numpy()
        outcomes_back = out_df.loc[out_idx_back[:]].to_numpy()
        payments_back = np.array([[size * (price - 1)*0.95 if n == True or n == 'True' else size * -1 if n == False or n == 'False' else size * 0 if n == 'VOID' else size * 0.5 * (price - 1)*0.95 if n == 'HALF WIN' else size * -0.5 if n == 'HALF LOSE' else 0 for n in market_array] for ((price,size),market_array) in zip(price_size_back, outcomes_back)])
        
    else:
        payments_back = []

    current_orders_lay = current_orders_df[(current_orders_df['side'] == 'LAY') & (current_orders_df['status'] == 'EXECUTION_COMPLETE')].loc[:, ['marketId', 'selectionId', 'handicap']].to_numpy()
    if current_orders_lay.size !=0:
        selections_lay = pd.concat([bet_details[(bet_details['Market ID'] == m) & (bet_details['Selection ID'] == s) & (bet_details['Handicap'] == h)].loc[:, ['Market Name', 'Selection Name']] for m,s,h in current_orders_lay])
        out_idx_lay = [(a,b,'Lay') for (a,b) in list(selections_lay.itertuples(index=False, name=None))]
        price_size_lay = current_orders_df[(current_orders_df['side'] == 'LAY') & (current_orders_df['status'] == 'EXECUTION_COMPLETE')][['price', 'size']].to_numpy()
        outcomes_lay = out_df.loc[out_idx_lay[:]].to_numpy()
        payments_lay = np.array([[((price - 1) ** (-1))*.95 if n == True or n == 'True' else -1 if n == False or n == 'False' else 0 if n == 'VOID' else 0.5 * ((price - 1) ** (-1))*0.95 if n =='HALF WIN' else -0.5 if n == 'HALF LOSE' else 0 for n in market_array] for ((price,size),market_array) in zip(price_size_lay, outcomes_lay)])
    else:
        payments_lay = []

    if len(payments_back) == 0 and len(payments_lay) == 0:
        payoffs_bets_total = np.zeros(len(out_df.columns))
        payoffs_bets_df = pd.DataFrame({'Bet Total': payoffs_bets_total})
        # # payoffs_bets_df.loc['Bet Total', :] = payoffs_bets_total

    elif len(payments_lay) == 0:
        payoffs_bets = payments_back
        payoffs_bets_df = pd.DataFrame(payoffs_bets, index=pd.MultiIndex.from_tuples(out_idx_back, names=out_df.index.names), columns=out_df.columns)
        payoffs_bets_total = np.sum(payoffs_bets, axis=0)
        payoffs_bets_df.loc['Bet Total', :] = payoffs_bets_total

    elif len(payments_back) == 0:
        payoffs_bets = payments_lay
        payoffs_bets_df = pd.DataFrame(payoffs_bets, index=pd.MultiIndex.from_tuples(out_idx_lay, names=out_df.index.names), columns=out_df.columns)
        payoffs_bets_total = np.sum(payoffs_bets, axis=0)
        payoffs_bets_df.loc['Bet Total', :] = payoffs_bets_total

    else:
        payoffs_bets = np.vstack([payments_back, payments_lay])
        payoffs_bets_df = pd.DataFrame(payoffs_bets, index=pd.MultiIndex.from_tuples(out_idx_back + out_idx_lay, names=out_df.index.names), columns=out_df.columns)
        payoffs_bets_total = np.sum(payoffs_bets, axis=0)
        payoffs_bets_df.loc['Bet Total', :] = payoffs_bets_total

    payoffs_bets_df.to_csv(f'Bet_Payoffs_{home_team}_v_{away_team}.csv')

    hedge_scenarios = payoffs_bets_df.iloc[:-1, :]
    hedge_scenarios_total = payoffs_bets_df.loc['Bet Total', pd.IndexSlice[(range(3+1)), (range(3+1))]]


    if np.any(hedge_scenarios_total.to_numpy()[0] < -1): 
        print('bets are unbalanced. Rerun Linprog')
    else:
        print('Bets are balanced!')

else:
    payoffs_bets_df = []
    hedge_scenarios = []
    print('no bets active')

if len(current_orders_df) > 0:
    cancel_market_ids = current_orders_df[current_orders_df['status'] == 'EXECUTABLE'].loc[:, 'marketId']

    if len(cancel_market_ids) > 0:
        for i in cancel_market_ids.to_numpy():
            cancelled_order = trading.betting.cancel_orders(market_id=i)

        # Create a DataFrame to view the instruction report
        pd.Series(cancelled_order.cancel_instruction_reports[0].__dict__).to_frame().T
    else:
        pass
    
    current_orders_df.to_csv('current_orders.csv')
else:
    pass