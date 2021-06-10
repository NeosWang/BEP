import pandas as pd


path = "data/"


data_links = 'primaryschool.csv'
# data_links = 'primaryschool_sub.csv'

data_nodes = 'metadata_primaryschool.txt'
# data_nodes = 'metadata_primaryschool_sub.txt'

links_colnames = ['t', 'i', 'j', 'ci', 'cj']

nodes_colnames = ['id', 'class', 'gender']


df_links = pd.read_csv(path+data_links,
                       header=None,
                       names = links_colnames,
                       sep='\t')

df_nodes = pd.read_csv(path+data_nodes,
                       header=None,
                       names = nodes_colnames,
                       sep='\t')
df_nodes
count=0
idx =[]
for i in range(1,len(df_links)):
    if (df_links.at[i,'t'] - df_links.at[i-1,'t']) not in [0,20] :
        count+=1
        idx.append(i)
count
        
df_links.iloc[60620:60630]
df_links

31220/3600
117240 - 3600*24



len(df_nodes)