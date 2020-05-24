import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
import time
# dataset  = []
# with open('../../dataSource/market/dataset.txt','r') as f:
#     for line in f.readlines():
#         words =line.strip().split(',')
#         dataset.append(words)

#     f.close()
# te = TransactionEncoder()
# te_ary = te.fit(dataset).transform(dataset)
# df = pd.DataFrame(te_ary, columns=te.columns_)

#df = pd.read_csv('../../dataSource/market/marketBool.csv')
#print(df.head().to_string())

#frequent_itemsets=fpgrowth(df, min_support=0.01,use_colnames=True)
#frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))

#association_rule=association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

#print(association_rule.head(15).to_string())
#association_rule.to_csv('../../output/dataMining/FP_Growth_ar.csv',index=False)



def fp_growth(dataframe,confidence=0.1,support=0.1,nbtransaction=None):
    if(nbtransaction==None):
        nbtransaction=dataframe.shape[0]
    df_tmp=dataframe.sample(nbtransaction,replace=False)
    frequent_itemsets = fpgrowth(df_tmp, min_support=support, use_colnames=True)
    if(frequent_itemsets.shape[0]>0):
        association_rule = association_rules(frequent_itemsets, metric="confidence", min_threshold=confidence)
        return association_rule
    else:
        return None

# support =[0.001,0.002,0.003,0.004,0.005,0.01,0.02,0.03,0.04,0.05,0.1,0.2,0.3,0.4,0.5,1]
# confs=[_/10 for _ in range (1,11,1)]
# transNumber=[_ for _ in range(980,10000,980)]
# colomns=['support','confidance','time','transaction_number']
# result=[]
# for numTrans in transNumber:
#     for sup in support:
#         for conf in confs:
#             start_time = time.time()
#             fp_growth(df,confidance=conf,support=sup,nbtransaction=numTrans)
#             endingTime=(time.time() - start_time)
#             print("--- %s seconds ---" % endingTime)
#             result.append([sup,conf,endingTime,numTrans])

# #%%
# output =  pd.DataFrame(result,columns=colomns)
# output.to_csv('../../output/dataMining/FP_Growth_performance.csv',index=False)
        



