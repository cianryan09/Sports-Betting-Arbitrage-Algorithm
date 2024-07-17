from bf_lightweight import betfairlightweight, trading, pd
from event_IDs import event_id

# Define a market filter
market_types_filter = betfairlightweight.filters.market_filter(event_ids=[event_id])

# Request market types
market_types = trading.betting.list_market_types(
        filter=market_types_filter
)

# Create a DataFrame of market types
market_types_df = pd.DataFrame({
    'Market Type': [market_type_object.market_type for market_type_object in market_types]
})

market_types_df.to_csv('market_types.csv')