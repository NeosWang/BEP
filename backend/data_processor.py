import pandas as pd
import csv
import json

path = "backend/data/"
# path = "data/"

links_colnames = ['t', 'i', 'j', 'ci', 'cj']

nodes_colnames = ['id', 'class', 'gender']


def get_data():
    with open(path+'primaryschool.csv') as file:
        reader = csv.DictReader(file, fieldnames=links_colnames, delimiter="\t")
        links = json.dumps(list(reader))
        
    with open(path+'metadata_primaryschool.txt') as file:
        reader = csv.DictReader(file, fieldnames=nodes_colnames, delimiter="\t")
        nodes = json.dumps(list(reader))
        
    return links, nodes
   
   

