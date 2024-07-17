from bf_lightweight import betfairlightweight, trading, pd
from event_types import soccer
from competition_IDs import competition_id, competition_name
from datetime import datetime, timezone, timedelta

next_n_days = 3
n_days = datetime.now(timezone.utc) + timedelta(days=next_n_days)
now = datetime.now(timezone.utc)

# Define a market filter
soccer_event_filter = betfairlightweight.filters.market_filter(
    event_type_ids=[soccer],
    market_countries=[None],
    competition_ids=[competition_id],
    market_start_time={
        'to': (n_days).strftime("%Y-%m-%dT%TZ")
    }
)


# Get a list of all soccer events as objects
all_soccer_events = trading.betting.list_events(
    filter=soccer_event_filter
)

all_soccer_events_n_days = pd.DataFrame({
    'Event Name': [event_object.event.name for event_object in all_soccer_events],
    'Event ID': [event_object.event.id for event_object in all_soccer_events],
    'Event Venue': [event_object.event.venue for event_object in all_soccer_events],
    'Country Code': [event_object.event.country_code for event_object in all_soccer_events],
    'Time Zone': [event_object.event.time_zone for event_object in all_soccer_events],
    'Open Date': [event_object.event.open_date for event_object in all_soccer_events],
    'Market Count': [event_object.market_count for event_object in all_soccer_events]
})

home_team = 'Solihull Moors'
away_team = 'Birmingham'

# print(all_soccer_events_n_days)

all_soccer_events_n_days.to_csv(f'Soccer_Events_{now.strftime("%Y-%m-%d")}_to_{n_days.strftime("%Y-%m-%d")}.csv')

# event_id = all_soccer_events_n_days.loc[all_soccer_events_n_days['Event Name'] == f'{home_team} v {away_team}', 'Event ID'].values[0]
event_id = 33422928

# print(all_soccer_events_n_days.loc[all_soccer_events_n_days['Event Name'] == f'{competition_name}', 'Event ID'].values[0])