from calculate_payoffs import payoffs_total
from bf_lightweight import pd, np

print(len(payoffs_total))
# payoffs_total.loc[pd.IndexSlice[m, :,:], :]
# print(print(payoffs_total.index.levels))

r_array = np.random.rand(len(payoffs_total))
print(r_array)
mkts = [m[0] for m in payoffs_total.iloc[:,0].groupby('Market', sort=False)]

# print([payoffs_total.loc[pd.IndexSlice[m, :,:], pd.IndexSlice[0,0]].to_numpy() for m in mkts])