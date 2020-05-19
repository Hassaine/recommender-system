import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
# dataset  = []
# with open('../../dataSource/market/dataset.txt','r') as f:
#     for line in f.readlines():
#         words =line.strip().split(',')
#         dataset.append(words)

#     f.close()
# te = TransactionEncoder()
# te_ary = te.fit(dataset).transform(dataset)
# df = pd.DataFrame(te_ary, columns=te.columns_)

df = pd.read_csv('../../dataSource/market/marketBool.csv')
#print(df.head().to_string())

frequent_itemsets=fpgrowth(df, min_support=0.01,use_colnames=True)
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))

association_rule=association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
#%%
#print(association_rule.head(15).to_string())
association_rule.to_csv('../../output/dataMining/FP_Growth_ar.csv',index=False)

