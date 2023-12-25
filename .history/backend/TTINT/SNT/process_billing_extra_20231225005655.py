import pandas as pd
from datetime import datetime


def __get_cbcode(s):
    try:
        return s.split('|')[0].strip()
    except:
        return None

def __conver_time_customs(d):
    return d if pd.isna(d) else f"{ datetime.strptime( d,'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')}+0000"

def __conver_time_logistics(d):
    return d if pd.isna(d) else datetime.strptime( d,'%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")

def __extract_time(col_199, col_3034, col_3032):
    if not pd.isna(col_199):
        return  col_199
    if not pd.isna(col_3034):
        return col_3034
    if not pd.isna(col_3032):
        return  col_3032
    
def __extract_status(col_199, col_3034, col_3032):
    if not pd.isna(col_199):
        return "199"
    if not pd.isna(col_3034):
        return "3034"
    if not pd.isna(col_3032):
        return "3032"



def process_billing_extra(path_in, is_customs=False):
    cols_map={
        "Customer Item Id":"lpcode",
        "Barcode":"barcode",
        "Manifest Product Code":"product",
    }
    df = pd.read_excel(path_in,dtype=str)
    df = df.rename(columns=cols_map)
    df['cbcode'] = df['Manifest RC'].apply(__get_cbcode)

    df["time"] = df.apply(lambda x: __extract_time(x['199 Event'],x[3034], x['3032 Event']), axis=1)
    df['status'] = df.apply(lambda x: __extract_status(x['199 Event'],x[3034], x['3032 Event']), axis=1)

    df['time'] = df['time'].apply(
        __conver_time_customs) if is_customs else df['time'].apply(
        __conver_time_logistics)
    return df[['barcode','lpcode','cbcode','product','status','time']]



