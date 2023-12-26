import concurrent.futures
import pandas as pd


def concurrent_df_tasks(df: pd.DataFrame, row_fuc, row_kwargs, res_fuc, res_kwargs):
    with concurrent.futures.ThreadPoolExecutor() as tpe:
        results = [tpe.submit(row_fuc, row, **row_kwargs)
                   for _, row in df.iterrows()]
        for f in concurrent.futures.as_completed(results):
            res_fuc(f.result(), **res_kwargs)
