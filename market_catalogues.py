from bf_lightweight import betfairlightweight, trading, pd
from event_IDs import event_id
from read_outcome_table import markets

market_catalogue_filter = betfairlightweight.filters.market_filter(event_ids=[event_id])

market_catalogues = trading.betting.list_market_catalogue(
    filter=market_catalogue_filter,
    max_results='100',
    sort='FIRST_TO_START'
)


market_catalogues_df = pd.DataFrame({
    'Market Name': [market_cat_object.market_name for market_cat_object in market_catalogues],
    'Market ID': [str(market_cat_object.market_id) for market_cat_object in market_catalogues],
    'Total Matched': [market_cat_object.total_matched for market_cat_object in market_catalogues],
}).sort_values(by='Total Matched', ascending=False)

market_catalogues_df.set_index('Market ID', inplace=True)
market_name_dict = {k: v for k,v in zip(market_catalogues_df.index.values, market_catalogues_df['Market Name'].values)}

market_catalogue_filtered = market_catalogues_df[market_catalogues_df['Market Name'].isin(markets)]
market_catalogue_filtered.to_csv('market_catalogue.csv')

market_list = market_catalogue_filtered['Market Name'].values