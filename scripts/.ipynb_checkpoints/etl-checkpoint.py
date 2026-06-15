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

def explore(df)
    df.head(5)
    return df

df = extract(RAW_PATH)
explore(df)