from bf_lightweight import betfairlightweight, trading, datetime, pd
from event_types import soccer

# Get a datetime object in a week and convert to string
datetime_in_a_week = (datetime.datetime.utcnow() + datetime.timedelta(weeks=1)).strftime("%Y-%m-%dT%TZ")

# Create a competition filter
competition_filter = betfairlightweight.filters.market_filter(
    event_type_ids=[soccer], # Soccer's event type id is 1
    market_start_time={
        'to': datetime_in_a_week
    })

# Get a list of competitions for soccer
competitions = trading.betting.list_competitions(
    filter=competition_filter
)

# Iterate over the competitions and create a dataframe of competitions and competition ids
soccer_competitions = pd.DataFrame({
    'Competition': [competition_object.competition.name for competition_object in competitions],
    'ID': [competition_object.competition.id for competition_object in competitions]
})
soccer_competitions.to_csv('all_competitions.csv')
competition_name = 'Friendly Matches'

competition_id = soccer_competitions.loc[soccer_competitions['Competition'] == competition_name, 'ID'].values[0]
print(competition_id)