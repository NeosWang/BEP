import pandas as pd

links_colnames=['t','i','j','ci','cj']
links = pd.read_csv('data/primaryschool.csv',sep="\t",header=None,names=links_colnames)

nodes_colnames=['id','class','gender']
nodes = pd.read_csv('data/metadata_primaryschool.txt',sep="\t", header=None, names=nodes_colnames)

nodes