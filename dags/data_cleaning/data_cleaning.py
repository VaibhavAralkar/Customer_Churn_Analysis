import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# --- Configuration ---
TABLE_NAME = "customer_data"
CLEANED_TABLE_NAME = f"{TABLE_NAME}_cleaned"
DB_NAME = "prediction_data"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "postgres"
DB_PORT = "5432"

# --- Required columns (keep in order) ---
REQUIRED_COLUMNS = [
    "customerid", "age", "gender", "tenure", "monthlycharges",
    "contracttype", "internetservice", "totalcharges", "techsupport", "churn"
]

# --- Connect to PostgreSQL ---
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# --- Step 1: Load data from PostgreSQL table ---
try:
    df = pd.read_sql_table(TABLE_NAME, con=engine)
    print(f"✅ Loaded table '{TABLE_NAME}' with {df.shape[0]} rows and {df.shape[1]} columns.")
except Exception as e:
    print(f"❌ Failed to read from PostgreSQL: {e}")
    exit()

# --- Step 2: Keep only required columns ---
missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
if missing_cols:
    print(f"❌ Missing columns in source table: {missing_cols}")
    exit()

df = df[REQUIRED_COLUMNS]  # Enforce column order

# --- Step 3: Handle missing values ---
df.replace(" ", np.nan, inplace=True)

# Convert 'totalcharges' to numeric safely
if "totalcharges" in df.columns:
    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors='coerce')

# Fill missing values
for col in df.columns:
    if df[col].isnull().any():
        if df[col].dtype == 'object':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

# --- Step 4: Convert binary columns to boolean ---
binary_map = {'Yes': True, 'No': False}
binary_cols = ['churn', 'techsupport']

for col in binary_cols:
    if col in df.columns:
        df[col] = df[col].map(binary_map)

# --- Step 5: Remove duplicates ---
original_count = df.shape[0]
df.drop_duplicates(inplace=True)
cleaned_count = df.shape[0]
print(f"🧹 Removed {original_count - cleaned_count} duplicate rows.")

# --- Step 6: Changeing ContractType column ---
contracttype_map = {
    'Month-to-Month': 'Monthly',
    'One-Year': 'Yearly',
    'Two-Year': '2-Yearly'
}

if 'contracttype' in df.columns:
    df['contracttype'] = df['contracttype'].map(contracttype_map).fillna(df['contracttype'])

# Convert 'totalcharges' to numeric safely
if "totalcharges" in df.columns:
    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors='coerce')


# Round 'totalcharges' to 2 decimal places
if 'totalcharges' in df.columns:
    df['totalcharges'] = df['totalcharges'].round(2)


# --- Step 7: Write cleaned data to new table ---
try:
    df.to_sql(CLEANED_TABLE_NAME, engine, if_exists='replace', index=False)
    print(f"✅ Cleaned data written to '{CLEANED_TABLE_NAME}' with {df.shape[0]} rows.")
except Exception as e:
    print(f"❌ Failed to write cleaned data to PostgreSQL: {e}")
