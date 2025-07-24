import os
import pandas as pd
import psycopg2
from psycopg2 import sql

# Database connection config
DB_CONFIG = {
    'dbname': 'ecommerce',
    'user': 'postgres',
    'password': 'password,
    'host': 'localhost',
    'port': '5432'
}

# Path to folder containing CSV files
CSV_FOLDER_PATH = './ecommerce_dataset'  # <-- change this to your folder path

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def load_csv_to_postgres(csv_file, table_name, conn):
    df = pd.read_csv(csv_file)

    with conn.cursor() as cur:
        # Create table if it doesn't exist (basic columns, adjust types as needed)
        create_cols = ', '.join([
            f'"{col}" TEXT' for col in df.columns
        ])
        cur.execute(sql.SQL(f"""
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                {create_cols}
            );
        """))

        # Clear existing data (optional)
        cur.execute(sql.SQL(f'DELETE FROM "{table_name}";'))

        # Insert data
        for _, row in df.iterrows():
            insert_query = sql.SQL(f"""
                INSERT INTO "{table_name}" ({','.join([f'"{col}"' for col in df.columns])})
                VALUES ({','.join(['%s'] * len(df.columns))});
            """)
            cur.execute(insert_query, list(row.values))

    conn.commit()
    print(f"✅ Inserted data into {table_name}")

def main():
    conn = get_connection()

    for file_name in os.listdir(CSV_FOLDER_PATH):
        if file_name.endswith('.csv'):
            table_name = file_name.replace('.csv', '').lower()
            csv_path = os.path.join(CSV_FOLDER_PATH, file_name)
            load_csv_to_postgres(csv_path, table_name, conn)

    conn.close()
    print("🎉 All CSVs loaded into PostgreSQL.")

if __name__ == '__main__':
    main()
