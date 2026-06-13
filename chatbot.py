import os
import re
from dotenv import load_dotenv
import gradio as gr

from sqlalchemy import text
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Database setup - SQLite only for HF deployment
# -----------------------------
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "northwind.db")

if not os.path.exists(db_path):
    raise FileNotFoundError(f"northwind.db not found at {db_path}")

db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
DB_DIALECT = "sqlite"
print(f"✅ Database loaded from: {db_path}")
print(f"🗄️ Database dialect: {DB_DIALECT}")

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
You are a SQL expert for the Northwind SQLite database.

The database has these tables:
- Customers: CustomerID, CompanyName, ContactName, City, Country, Phone
- Products: ProductID, ProductName, Category, UnitPrice, UnitsInStock
- Orders: OrderID, CustomerID, OrderDate, ShipCity, ShipCountry

Rules:
- Use STRFTIME('%Y', OrderDate) for year filtering
- Use STRFTIME('%m', OrderDate) for month filtering
- ONLY generate SELECT queries
- Return ONLY the raw SQL, no explanation, no markdown, no backticks

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
        raise ValueError("No SELECT query found in response")
    return match.group(1).strip().rstrip(";") + ";"


def sql_to_markdown(sql: str) -> str:
    with db._engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        cols = list(result.keys())

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
        response = query_chain.invoke({"question": question})
        sql_query = extract_sql(response)
        print("🔹 Generated SQL:", sql_query)

        forbidden = ("drop", "delete", "update", "insert", "alter", "truncate")
        if any(word in sql_query.lower() for word in forbidden):
            return "❌ This operation is not allowed."

        return sql_to_markdown(sql_query)

    except Exception as e:
        return f"❌ Error: {str(e)}"

# -----------------------------
# Gradio UI
# -----------------------------
demo = gr.Interface(
    fn=chat_with_database,
    inputs=gr.Textbox(
        label="Ask a question about the Northwind database",
        placeholder="e.g., Show all customers from Germany",
        lines=3
    ),
    outputs=gr.Markdown(label="Result"),
    title="🤖 Northwind Database Chatbot",
    description="All answers are shown as tables.",
    examples=[
        "Show all customers from Germany",
        "Top 5 most expensive products",
        "List all products in the Beverages category",
        "How many orders were placed in 2024?",
        "Show all orders from July 2024"
    ]
)

if __name__ == "__main__":
    print("🚀 Starting Northwind Chatbot...")
    demo.launch(server_name="0.0.0.0", server_port=7860)