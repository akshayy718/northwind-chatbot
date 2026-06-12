# 🤖 Northwind Database Chatbot

An AI-powered chatbot that converts natural language questions into SQL queries and returns answers in plain English. Built using LangChain, Groq's Llama 3.3 70B model, and Microsoft SQL Server.

---

## 📸 Screenshots

![Screenshot1](screenshots/Screenshot%202026-06-11%20135228.png)
![Screenshot2](screenshots/Screenshot%202026-06-11%20135257.png)
![Screenshot3](screenshots/Screenshot%202026-06-11%20135314.png)
![Screenshot4](screenshots/Screenshot%202026-06-11%20135340.png)
![Screenshot5](screenshots/Screenshot%202026-06-11%20135410.png)
![Screenshot6](screenshots/Screenshot%202026-06-11%20135503.png)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.13 | Core programming language |
| LangChain | AI/LLM framework |
| Groq API (Llama 3.3 70B) | Natural language to SQL generation |
| Microsoft SQL Server | Database backend |
| Northwind Database | Sample ERP dataset |
| Gradio | Web UI interface |
| SQLAlchemy | Database ORM |
| PyODBC | SQL Server connection driver |

---

## ✨ Features

- 💬 Natural language to SQL conversion
- 🗄️ Microsoft SQL Server integration
- 🔒 Read-only query enforcement (SELECT only)
- 🌐 Web-based Gradio UI
- ⚡ Fast responses using Groq's Llama 3.3 70B
- 🔄 Automatic fallback to SQLite (demo mode)
- 📊 Returns results in clear natural language

---

## 🚀 How to Run

### Prerequisites
- Python 3.11+
- Microsoft SQL Server (or SQL Server Express)
- ODBC Driver 17 for SQL Server
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

**Step 1: Clone the repository**
```bash
git clone https://github.com/akshayy718/northwind-chatbot.git
cd northwind-chatbot
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Create `.env` file**
```
GROQ_API_KEY=your_groq_api_key_here
```

**Step 4: Configure SQL Server in `config.py`**
```python
DATABASE_CONFIG = {
    "server": "YOUR_SERVER_NAME",
    "database": "Northwind",
    "username": "",
    "password": ""
}
```

**Step 5: Run the chatbot**
```bash
python chatbot.py
```

**Step 6: Open in browser**
```
http://localhost:7860
```

---

## 💬 Example Questions

- "How many customers are there?"
- "Show all customers from Germany"
- "What are the top 5 most expensive products?"
- "How many orders were placed in 1997?"
- "What is the total revenue from all orders?"
- "Who are the top 10 customers by number of orders?"
- "Show all products in the Beverages category"

---

## 📁 Project Structure

```
northwind-chatbot/
├── chatbot.py          # Main chatbot application
├── config.py           # Database configuration
├── requirements.txt    # Python dependencies
├── instnwnd.sql        # Northwind database setup script
├── .gitignore          # Git ignore rules
├── screenshots/        # Output screenshots
└── README.md           # Project documentation
```

---

## 🔧 How It Works

```
User Question
     ↓
LangChain + Groq LLM
     ↓
SQL Query Generated
     ↓
Microsoft SQL Server
     ↓
Results Fetched
     ↓
Natural Language Answer
     ↓
Gradio UI Display
```

---

## 👨‍💻 Author

**Akshay Santhosh**
- GitHub: [@akshayy718](https://github.com/akshayy718)
- Email: akshaysanthosh718@gmail.com
- 
