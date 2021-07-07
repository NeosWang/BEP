import pandas as pd
import os

# path = "data/"
# path = "backend/data/"

# data_links = 'primaryschool.csv'

# data_nodes = 'metadata_primaryschool.txt'

# sep = "\t"


# def preview(path, filename , sep, header = 0):
#     df = pd.read_csv(path + filename, sep = sep, header = header)
#     df = df.head()
#     return df.to_dict(orient='split')


def process(dict,is_relationships, is_preview=False, is_demo=False):
    header = None if dict['noneHeader'] else 0
    df = pd.read_csv(
        os.path.join(dict['path'],
        dict['filename']), 
        sep = dict['sep'], 
        header = header,
        engine='python')
    if 'columns' in dict:
        df.columns = dict['columns']
        if is_relationships:
            df = df.rename(columns={'time': 't'})[['t','i','j']]
            
    if is_preview and is_demo:
        if is_relationships:
            df.columns = ['time','i','j','3','4']            
        else:
            df.columns = ['id','class','gender']
            
    if is_preview:
        df = df.head()
        return df.to_dict(orient='split')
    else:       
        return df.to_dict(orient='records')
    