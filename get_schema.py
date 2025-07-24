import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()

# Check for required environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Missing required environment variable: DATABASE_URL")

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

def get_table_schemas():
    schema_docs = []
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        col_defs = [f"{col['name']} {col['type']}" for col in columns]
        doc = f"Table: {table_name}\nColumns:\n" + "\n".join(col_defs)
        schema_docs.append({"table": table_name, "schema": doc})
    return schema_docs

if __name__ == "__main__":
    schemas = get_table_schemas()
    print(schemas)
