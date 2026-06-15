import pandas as pd #read, clean, data
import numpy as np #math operations
import sqlite3 #local DB
import os #file paths

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "Sample - Superstore.csv")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "superstore_clean.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "superstore.db")

def extract(path):
    print("Extracting data...")
    df = pd.read_csv(path, encoding="latin-1") #handle special characters
    print(f" Loaded {len(df)} rows, {len(df.columns)} columns")
    return df

def explore(df):
    print(df.head(5))
    print(df.shape)
    print(df.dtypes)
    print(df.isnull().sum())


def transform(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df['Postal Code'] = df['Postal Code'].astype(str)
    df = df.drop_duplicates()
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip() #strip whitespace
    df['Revenue'] = df['Sales'] * df['Quantity']
    df['Profit Margin'] = (df['Profit'] / df['Sales']).round(4)
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month
    df['Customer Name'] = df['Customer Name'].str.encode('ascii', errors='ignore').str.decode('ascii')
    print(df.shape)
    print("Transformation complete.")
    return df

def load(df):
    df.to_csv(PROCESSED_PATH, index = False)
    print(f"Saved CSV to {PROCESSED_PATH}")
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('superstore', conn, if_exists='replace', index=False)
    print(f"Loaded {len(df)} rows into SQLite table 'superstore'")
    conn.close()
    print("DB connection closed.")

def main():
    df = extract(RAW_PATH)
    explore(df)
    df = transform(df)
    #print(df)
    df = load(df)

if __name__ == "__main__":
    main()