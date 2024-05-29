import pandas as pd
import numpy as np
import os

def sanitize(df):
    return df.applymap(
        lambda x: x.replace(',', '').replace(' ', '').strip() if isinstance(x, str) else '' if pd.isna(x) else x)

def load_df(filename, file_path='/usr/local/airflow/dags/input'):
    full_path = os.path.join(file_path, f'{filename}.csv')
    try:
        df = pd.read_csv(full_path)
        print(f"File '{filename}.csv' loaded successfully from '{file_path}'.")
        return df
    except FileNotFoundError:
        print(f"Error: The file '{filename}.csv' was not found in the directory '{file_path}'.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{filename}.csv' is empty.")
    except pd.errors.ParserError:
        print(f"Error: The file '{filename}.csv' could not be parsed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")




