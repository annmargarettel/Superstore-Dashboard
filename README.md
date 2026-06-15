# Superstore Sales Analytics Dashboard

## Project Overview
A full end-to-end data analytics project analyzing retail sales data from the Kaggle Superstore dataset. Built for marketing and business stakeholders to explore revenue trends, product performance, and customer behavior.

## Tech Stack
| Python (pandas, NumPy) | Data cleaning and feature engineering |
| SQLite | Local database storage |
| SQL | Data aggregation and querying |
| Streamlit | Interactive web dashboard |
| Plotly | Data visualizations |
| Power BI | Business intelligence dashboard |
| Excel | Pivot tables and customer lookup report |
| Docker | App containerization |

## Project Structure
superstore_project/
├── data/
│   ├── raw/                    ← original dataset
│   ├── processed/              ← cleaned CSV
│   └── superstore.db           ← SQLite database
├── scripts/
│   ├── etl.py                  ← ETL pipeline
│   └── queries.py              ← SQL queries
├── app.py                      ← Streamlit dashboard
├── Dockerfile                  ← container setup
└── requirements.txt            ← dependencies

## How to Run

### Option 1 — Local
```bash
# Step 1: Run the ETL pipeline
python scripts/etl.py

# Step 2: Launch the dashboard
streamlit run app.py
```

### Option 2 — Docker
```bash
docker build -t superstore-dashboard .
docker run -p 8501:8501 superstore-dashboard
```

## Key Insights
- **Tables and Bookcases are unprofitable** despite high sales volume,
  likely due to heavy discounting
- **West region leads in total revenue ($3.6M)** 
- **Tech products drive the most sales and profit** 
