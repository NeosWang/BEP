import pandas as pd
import json

f = "Manifest TSLCOMBID301223  B.xlsx"

product_code = "IFRXL"

df = pd.read_excel(f)
df = df[df['Product']==product_code]

delivery = df['Delivery'][0]
delivery

nest = {}

for index, row in df.iterrows():
    if row['PostNL mailbagID'] in nest:
        nest[row['PostNL mailbagID']].append(row['Item barcode'])
    else:
        nest[row['PostNL mailbagID']] = [row['Item barcode']]
        
nest = { key:list(set(nest[key])) for key in nest}

for key,value in nest.items():
    

    payload = {
        "type": "ASSISTLABEL",
        "hawb": delivery,
        "assistlabel_item": {
            "assistlabel": key,
            "receptacle_type": "BG",
            "format": "E",
            "product_code": product_code,
            "items":sorted(value)
        }
    }
    print(json.dumps(payload))
    
    
len(df['Item barcode'].unique())