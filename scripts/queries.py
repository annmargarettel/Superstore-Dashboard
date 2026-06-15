import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "data", "superstore.db")
Q1_PATH = os.path.join(BASE_DIR, "data", "rev_by_mo.csv")
Q2_PATH = os.path.join(BASE_DIR, "data", "top_prod.csv")
Q3_PATH = os.path.join(BASE_DIR, "data", "sales_perf.csv")
Q4_PATH = os.path.join(BASE_DIR, "data", "cust_summ.csv")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    print("Connected to database.")
    return conn

def revenue_by_month():
    conn = get_connection()
    query = """
    SELECT [Order Year], [Order Month],ROUND(SUM(Revenue), 2) AS Total_Revenue
            FROM superstore
    GROUP BY [Order Year], [Order Month]
    ORDER BY [Order Year], [Order Month]
    """
    
    df = pd.read_sql(query, conn)

    print("Revenue by Month:")
    print(df)

    df.to_csv(Q1_PATH, index = False)
    print(f"Saved CSV to {Q1_PATH}")

    conn.close()
    print("Connection closed.")

def top_products():
    conn = get_connection()

    query = """
    SELECT [Product Name], ROUND(SUM(Revenue), 2) AS Total_Revenue, COUNT(*) AS Total_Orders
        FROM superstore
    GROUP BY [Product Name]
    ORDER BY [Total_Revenue] DESC
    LIMIT 10
    """

    df = pd.read_sql(query, conn)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(df)

    df.to_csv(Q2_PATH, index = False)
    print(f"Saved CSV to {Q2_PATH}")

    conn.close()
    print("Connection closed.")

def sales_by_region():
    conn = get_connection()

    query = """
    SELECT [Region], ROUND(SUM(Revenue), 2) AS Total_Revenue, COUNT(*) AS Total_Orders, ROUND(AVG(Sales), 2) AS Avg_Order_Value
        FROM superstore
    GROUP BY [Region]
    ORDER BY [Total_Revenue] DESC
    """

    df = pd.read_sql(query, conn)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(df)

    df.to_csv(Q3_PATH, index = False)
    print(f"Saved CSV to {Q3_PATH}")

    conn.close()
    print("Connection closed.")

def customer_summary():
    conn = get_connection()

    query = """
    SELECT [Customer ID], [Customer Name], [Segment], COUNT(DISTINCT [Order ID]) AS Total_Orders, ROUND(SUM(Revenue), 2) AS Total_Revenue, MIN([Order Date]) AS First_Order, MAX([Order Date]) AS Last_Order
        FROM superstore
    GROUP BY [Customer ID], [Customer Name], [Segment]
    ORDER BY [Total_Revenue] DESC
    LIMIT 20
    """

    df = pd.read_sql(query, conn)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(df)

    df.to_csv(Q4_PATH, index = False)
    print(f"Saved CSV to {Q4_PATH}")

    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    revenue_by_month()
    top_products()
    sales_by_region()
    customer_summary()
    