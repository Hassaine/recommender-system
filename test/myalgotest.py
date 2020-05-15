


#%%
import os,sys
os.chdir(os.path.dirname(sys.argv[0]))
dirpath = os.getcwd()
print("current directory is : " + dirpath)
foldername = os.path.basename(dirpath)
print("Directory name is : " + foldername)

#%%
import pandas as pd
ratingsPath = '../dataSource/moviesLen/ratings.csv'
df1 = pd.read_csv(ratingsPath)



