from io import StringIO
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def pandas_read_tsv_str(csv_str):
    return pd.read_csv(StringIO(csv_str), sep="\t")
