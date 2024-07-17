from collections import OrderedDict
from bf_lightweight import pd
from event_IDs import home_team, away_team

outcome_df = pd.read_csv('Solihull_Moors_v_Birmingham_20240717.csv', index_col=[0,1,2], header=[0,1])

# Convert the MultiIndex columns to integers
outcome_df.columns = pd.MultiIndex.from_tuples([(int(h), int(a)) for h, a in outcome_df.columns], names = [home_team, away_team])

markets = list(set(outcome_df.index.get_level_values(level=0)))
markets_idx = outcome_df.index.values

result_dict = OrderedDict(
    (key, list(OrderedDict.fromkeys(item[1] for item in markets_idx if item[0] == key)))
    for key in OrderedDict.fromkeys(item[0] for item in markets_idx)
)
# Sort the MultiIndex columns
outcome_df = outcome_df.sort_index(axis=1)

home_score = 0
away_score = 1

# f_string = f"('{home_score}', '{away_score}')"

# score_dict = {m: n for n, m in enumerate(outcome_df.columns.values)}
# idx = score_dict[(str(home_score), str(away_score))]

# outcome_df.columns = pd.MultiIndex.from_tuples(outcome_df.columns).sortlevel(0)[0]

outcome_df = outcome_df.loc[:, pd.IndexSlice[home_score:, away_score:]]

outcome_df.to_csv('outcome_df.csv')

# print(outcome_df.loc[:, pd.IndexSlice[(range(1,2), range(1,2))]])