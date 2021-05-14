import pandas as pd


# path = "data/"
# path = "backend/data/"

# data_links = 'primaryschool.csv'

# data_nodes = 'metadata_primaryschool.txt'

# sep = "\t"


def preview(path, data , sep, header = 0):
    df = pd.read_csv(path + data, sep = sep, header = header)
    df = df.head()
    return df.to_json(orient='split')

