import pandas as pd
import csv
import json

import pandas as pd

# path = "data/"

path = "backend/data/"

# data_links = 'primaryschool.csv'
data_links = 'primaryschool_sub.csv'

# data_nodes = 'metadata_primaryschool.txt'
data_nodes = 'metadata_primaryschool_sub.txt'

links_colnames = ['t', 'i', 'j', 'ci', 'cj']

nodes_colnames = ['id', 'class', 'gender']


def get_data():
    with open(path+data_links) as file:
        reader = csv.DictReader(
            file, fieldnames=links_colnames, delimiter="\t")
        links = json.dumps(list(reader))

    with open(path+data_nodes) as file:
        reader = csv.DictReader(
            file, fieldnames=nodes_colnames, delimiter="\t")
        nodes = json.dumps(list(reader))
    return links, nodes