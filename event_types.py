from bf_lightweight import trading, pd

# Grab all event type ids. This will return a list which we will iterate over to print out the id and the name of the sport
event_types = trading.betting.list_event_types()

sport_ids = pd.DataFrame({
    'Sport': [event_type_object.event_type.name for event_type_object in event_types],
    'ID': [event_type_object.event_type.id for event_type_object in event_types]
}).set_index('Sport').sort_index()

sport = 'Soccer'

soccer = sport_ids.loc[sport, 'ID']

# soccer = 1