from flask import render_template, request
from datetime import datetime
import pandas as pd
from backend._cainiao import CAINIAO
from backend._concurrent import concurrent_df_tasks
from backend._file import File
import backend._config as _config


def home():
    return render_template('snt_billing_repush.html')




# region[ process_billing_extra ]

def process_billing_extra(file, is_customs=False):
    cols_map = {
        "Customer Item Id": "lpcode",
        "Barcode": "barcode",
        "Manifest Product Code": "product",
    }
    df = pd.read_excel(file, dtype=str)
    df = df.rename(columns=cols_map)
    df['cbcode'] = df['Manifest RC'].apply(__get_cbcode)

    df["time"] = df.apply(lambda x: __extract_time(
        x['199 Event'], x[3034], x['3032 Event']), axis=1)
    df['status'] = df.apply(lambda x: __extract_status(
        x['199 Event'], x[3034], x['3032 Event']), axis=1)

    df['time'] = df['time'].apply(
        __conver_time_customs) if is_customs else df['time'].apply(
        __conver_time_logistics)
    return df[['barcode', 'lpcode', 'cbcode', 'product', 'status', 'time']]


def __get_cbcode(s):
    try:
        return s.split('|')[0].strip()
    except:
        return None


def __conver_time_customs(d):
    return d if pd.isna(d) else f"{ datetime.strptime( d,'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')}+0000"


def __conver_time_logistics(d):
    return d if pd.isna(d) else datetime.strptime(d, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")


def __extract_time(col_199, col_3034, col_3032):
    if not pd.isna(col_199):
        return col_199
    if not pd.isna(col_3034):
        return col_3034
    if not pd.isna(col_3032):
        return col_3032


def __extract_status(col_199, col_3034, col_3032):
    if not pd.isna(col_199):
        return "199"
    if not pd.isna(col_3034):
        return "3034"
    if not pd.isna(col_3032):
        return "3032"

# endregion



# region[ repush_df_billing ]
    
def repush_df_billing(df, report_name):
    __repush_df_billing_all(df, report_name)
    __repush_df_billing_false(report_name)



def __repush_df_billing_all(df, report_name):
    report_path = f"{_config.UPLOAD_FOLDER}\{report_name}"

    df_list = __split_df(df, 50)
    for d in df_list:
        concurrent_df_tasks(
            df=d,
            row_fuc=__push_row,
            row_kwargs={"is_customs": 0},
            res_fuc=File.csv_add_records,
            res_kwargs={"file": report_path}
        )
    return


def __repush_df_billing_false(report_name):
    report_path = f"{_config.UPLOAD_FOLDER}\{report_name}"

    df = pd.read_csv(report_path,dtype=str)
    df_false = df[df['success']=='False']
    false_before = len(df_false)
    if not false_before:
        return
    df[df['success']!='False'].to_csv(report_path, index=False)
    for idx, row in df_false.iterrows():
        e = __push_row(row = row, is_customs=False)
        File.csv_add_records(e, report_path)

    df = pd.read_csv(report_path,dtype=str)
    df_false = df[df['success']=='False']
    false_after = len(df_false)
    if false_before == false_after:
        return
    __repush_df_billing_false(report_name)


def __split_df(df, n) -> list:
    output = []
    max = len(df)
    start = 0
    while 1:
        if start + n > max:
            output.append(df.iloc[start:max])
            break
        else:
            output.append(df.iloc[start:start+n])
        start += n
    return output


def __push_row(row, is_customs):
    e = {
        'barcode': row['barcode'],
        'lpcode': row['lpcode'],
        'cbcode': row['cbcode'],
        'product': row['product'],
        'status': row['status'],
        'time': row['time'],
        'msg_type': None,
        'success': None,
        'res': None,
    }

    cainiao = CAINIAO(
        env='prod',
        product_code=row['product']
    )
    if e['time']:
        e['msg_type'], e['success'], e['res'] = cainiao.tracking_event_callback(
            barcode=e['barcode'],
            lpcode=e['lpcode'],
            event=e['status'],
            opTime=row['time'])
    return e

# endregion
