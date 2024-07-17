from bf_lightweight import betfairlightweight, trading, pd
from market_catalogues import market_catalogue_filtered, market_name_dict
from read_outcome_table import result_dict

def process_runner_books(market_id, market_name_dict, result_dict, runner_books):
    '''
    This function processes the runner books and returns a DataFrame with the best back/lay prices + vol for each runner
    :param runner_books:
    :return:
    '''

    market_id_list = [str(market_id)] * len(runner_books)

    market_name_list = [market_name_dict[market_id]] * len(runner_books)

    selection_names = result_dict[market_name_dict[market_id]]

    best_back_prices = [runner_book.ex.available_to_back[0].price
                        if runner_book.ex.available_to_back
                        else 1.01
                        for runner_book
                        in runner_books]
    best_back_sizes = [runner_book.ex.available_to_back[0].size
                       if runner_book.ex.available_to_back
                       else 1.01
                       for runner_book
                       in runner_books]

    best_lay_prices = [runner_book.ex.available_to_lay[0].price
                       if runner_book.ex.available_to_lay
                       else 1000.0
                       for runner_book
                       in runner_books]
    best_lay_sizes = [runner_book.ex.available_to_lay[0].size
                      if runner_book.ex.available_to_lay
                      else 1.01
                      for runner_book
                      in runner_books]
    
    selection_ids = [runner_book.selection_id for runner_book in runner_books]
    handicaps = [runner_book.handicap for runner_book in runner_books]
    last_prices_traded = [runner_book.last_price_traded for runner_book in runner_books]
    total_matched = [runner_book.total_matched for runner_book in runner_books]
    statuses = [runner_book.status for runner_book in runner_books]
    scratching_datetimes = [runner_book.removal_date for runner_book in runner_books]
    adjustment_factors = [runner_book.adjustment_factor for runner_book in runner_books]

    df = pd.DataFrame({
        'Market ID': market_id_list,
        'Market Name': market_name_list,
        'Selection Name': selection_names,
        'Selection ID': selection_ids,
        'Handicap': handicaps,
        'Best Back Price': best_back_prices,
        'Best Back Size': best_back_sizes,
        'Best Lay Price': best_lay_prices,
        'Best Lay Size': best_lay_sizes,
        'Last Price Traded': last_prices_traded,
        'Total Matched': total_matched,
        'Status': statuses,
        'Removal Date': scratching_datetimes,
        'Adjustment Factor': adjustment_factors
    })
    return df

# Create a price filter. Get all traded and offer data
price_filter = betfairlightweight.filters.price_projection(
    price_data=['EX_BEST_OFFERS']
)

market_id_list = market_catalogue_filtered.index.values

# Request market books
market_books = trading.betting.list_market_book(
    market_ids=list(market_id_list),
    price_projection=price_filter
)

# Grab the first market book from the returned list as we only requested one market 
# market_book = market_books
# print(result_dict[market_name_dict['1.230452429']])
# print(market_books[26:27][0].runners)
runners_df = pd.concat([process_runner_books(market_book.market_id, market_name_dict, result_dict, market_book.runners) for market_book in market_books[:]])
runners_df.set_index('Market ID', inplace=True)

runners_df.to_csv('Market_Books.csv')