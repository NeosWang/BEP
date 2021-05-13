import pandas as pd


path = "data/"

data_links = 'primaryschool.csv'

data_nodes = 'metadata_primaryschool.txt'

sep = "\t"


def getDataPreview(path, data, sep, header = None):

    df = pd.read_csv(path + data, sep = sep, header = header)
    return df


df = getDataPreview(path, data_nodes, sep)
df
