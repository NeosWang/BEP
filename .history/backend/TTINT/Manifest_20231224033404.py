import pandas as pd

f = "Manifest TSLCOMBID231223  B.xlsx"

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


payload = {
    "type": "ASSISTLABEL",
    "hawb": "TSLCOMBID211223",
    "assistlabel_item": {
        "assistlabel": "FRTSL0000002169600",
        "receptacle_type": "BG",
        "format": "E",
        "product_code": "IFRXL",
        "items": [
            


        ]
    }
}