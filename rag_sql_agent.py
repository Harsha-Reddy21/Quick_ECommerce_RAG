
import os
from pinecone import Pinecone, ServerlessSpec

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from sqlalchemy import create_engine
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabase
from dotenv import load_dotenv

load_dotenv()

required_env_vars = ["DATABASE_URL", "PINECONE_API_KEY", "GEMINI_API_KEY"]
for var in required_env_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Configure Google API key - the library expects GOOGLE_API_KEY environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = gemini_api_key

# Use cheaper Gemini Flash model instead of Pro
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
print("Existing indexes:", pc.list_indexes())

index_name = "sql-agent"

if index_name not in [idx.name for idx in pc.list_indexes()]:
    print(f"Creating index: {index_name}")
    pc.create_index(
        name=index_name,
        dimension=768,  
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print("Index created successfully")
else:
    print(f"Index {index_name} already exists")

# Get the index object
pinecone_index = pc.Index(index_name)
print("Connected to index:", index_name)

def get_relevant_tables(query: str, top_k: int = 5):
    query_vec = embedder.embed_query(query)
    matches = pinecone_index.query(vector=query_vec, top_k=top_k, include_metadata=True)
    return [match["metadata"]["table"] for match in matches["matches"]]

def get_sql_agent(allowed_tables):
    limited_db = SQLDatabase(engine, include_tables=allowed_tables)
    toolkit = SQLDatabaseToolkit(db=limited_db, llm=llm)
    agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True, handle_parsing_errors=True)
    return agent

