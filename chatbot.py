import os
import re
import urllib
from dotenv import load_dotenv
import gradio as gr

from sqlalchemy import create_engine, text

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Database setup
# -----------------------------
db_path = None

try:
    from config import DATABASE_CONFIG

    if DATABASE_CONFIG.get("username") and DATABASE_CONFIG.get("password"):
        params = urllib.parse.quote_plus(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DATABASE_CONFIG['server']};"
            f"DATABASE={DATABASE_CONFIG['database']};"
            f"UID={DATABASE_CONFIG['username']};"
            f"PWD={DATABASE_CONFIG['password']};"
        )
    else:
        params = urllib.parse.quote_plus(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DATABASE_CONFIG['server']};"
            f"DATABASE={DATABASE_CONFIG['database']};"
            f"Trusted_Connection=yes;"
        )

    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    db = SQLDatabase(engine)
    print("✅ Connected to SQL Server")

except ImportError:
    print("⚠️ config.py not found - Using SQLite (demo mode)")
    db_path = os.path.join(os.getcwd(), "northwind.db")

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}")

    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    print(f"✅ Database loaded from: {db_path}")

# -----------------------------
# Detect database dialect
# -----------------------------
url = str(db._engine.url).lower()
DB_DIALECT = "sqlserver" if "mssql" in url else "sqlite"
print("🗄️ Database dialect:", DB_DIALECT)

# -----------------------------
# Initialize LLM
# -----------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# -----------------------------
# SQL generation prompt
# -----------------------------
sql_prompt = PromptTemplate.from_template(
    """
You are a SQL expert.

Given a natural language question, write a valid SQL SELECT query
for the Northwind database.

Database type: {dialect}

Rules:
- Use correct table and column names
- If database type is:
  - sqlite → use STRFTIME for dates
  - sqlserver → use YEAR(), MONTH(), DAY()
- ONLY generate SELECT queries
- Return ONLY the SQL query
- Do NOT explain anything

Question: {question}
"""
)

query_chain = RunnablePassthrough() | sql_prompt | llm

# -----------------------------
# Helpers
# -----------------------------
def extract_sql(response):
    sql = response.content.strip()
    sql = re.sub(r"```sql|```", "", sql, flags=re.IGNORECASE)
    match = re.search(r"(select\s+.*)", sql, re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError("No SELECT query generated")
    return match.group(1).strip().rstrip(";") + ";"


def sql_to_markdown(sql: str) -> str:
    with db._engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        cols = result.keys()

    if not rows:
        return "No data found."

    md = "| " + " | ".join(cols) + " |\n"
    md += "| " + " | ".join(["---"] * len(cols)) + " |\n"

    for row in rows:
        md += "| " + " | ".join(str(v) for v in row) + " |\n"

    return md

# -----------------------------
# Chat function
# -----------------------------
def chat_with_database(question: str):
    try:
        response = query_chain.invoke({
            "question": question,
            "dialect": DB_DIALECT
        })

        sql_query = extract_sql(response)
        print("🔹 Generated SQL:", sql_query)

        # Safety guard
        forbidden = ("drop", "delete", "update", "insert", "alter", "truncate")
        if any(word in sql_query.lower() for word in forbidden):
            return "❌ This operation is not allowed."

        return sql_to_markdown(sql_query)

    except Exception:
        return "❌ I couldn’t answer that question due to a database error."

# -----------------------------
# Gradio UI
# -----------------------------
demo = gr.Interface(
    fn=chat_with_database,
    inputs=gr.Textbox(
        label="Ask a question about the Northwind database",
        placeholder="e.g., Who ordered in 1997?",
        lines=3
    ),
    outputs=gr.Markdown(label="Result"),
    title="🤖 Northwind Database Chatbot",
    description="All answers are shown as tables.",
    examples=[
        "Who ordered in 1997?",
        "How many orders were placed in 1997?",
        "Show all customers from Germany",
        "Top 5 most expensive products",
        "List all products in the Beverages category"
    ]
)

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    print("🚀 Starting Northwind Chatbot...")
    demo.launch(server_name="0.0.0.0", server_port=7860)
