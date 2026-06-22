<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0,FF7C00,FFA500,FFD700&height=200&section=header&fontSize=42&fontColor=fff&animation=fadeIn&fontAlignY=36" width="100%"/>
</div>

<div align="center">

<pre>
 ███╗   ██╗ ██████╗ ██████╗ ████████╗██╗  ██╗██╗    ██╗██╗███╗   ██╗██████╗ 
 ████╗  ██║██╔═══██╗██╔══██╗╚══██╔══╝██║  ██║██║    ██║██║████╗  ██║██╔══██╗
 ██╔██╗ ██║██║   ██║██████╔╝   ██║   ███████║██║ █╗ ██║██║██╔██╗ ██║██║  ██║
 ██║╚██╗██║██║   ██║██╔══██╗   ██║   ██╔══██║██║███╗██║██║██║╚██╗██║██║  ██║
 ██║ ╚████║╚██████╔╝██║  ██║   ██║   ██║  ██║╚███╔███╔╝██║██║ ╚████║██████╔╝
 ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝

 ██████╗██╗  ██╗ █████╗ ████████╗██████╗  ██████╗ ████████╗
██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝
██║     ███████║███████║   ██║   ██████╔╝██║   ██║   ██║   
██║     ██╔══██║██╔══██║   ██║   ██╔══██╗██║   ██║   ██║   
╚██████╗██║  ██║██║  ██║   ██║   ██████╔╝╚██████╔╝   ██║   
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝  ╚═════╝    ╚═╝  
</pre>

## 🔗 Live Demo

<div align="center">

| | Link | Description |
|--|------|-------------|
| 🤗 | [**huggingface.co/spaces/Akshay718/northwind-chatbot**](https://huggingface.co/spaces/Akshay718/northwind-chatbot) | Try the chatbot live — no setup needed |

</div>

> ⚠️ **Note:** Hosted on Hugging Face's free tier — if idle, the Space may take 15–30 seconds to wake up on first load. Subsequent queries respond instantly.

---
[![Live Demo](https://img.shields.io/badge/▶_Try_Live_Demo-Hugging_Face_Spaces-FF7C00?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/spaces/Akshay718/northwind-chatbot)
[![GitHub](https://img.shields.io/badge/GitHub-akshayy718-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/akshayy718/northwind-chatbot)
[![Groq AI](https://img.shields.io/badge/🤖_Groq_AI-llama--3.3--70b-FFA500?style=for-the-badge)](https://console.groq.com)

</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-FF7C00?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-FFA500?style=flat-square&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-llama--3.3--70b-FF7C00?style=flat-square)
![Gradio](https://img.shields.io/badge/Gradio-Web_UI-FFA500?style=flat-square)
![SQL Server](https://img.shields.io/badge/MS_SQL_Server-Backend-FF7C00?style=flat-square&logo=microsoftsqlserver&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-FFA500?style=flat-square)

</div>

---

## 📌 Overview

An **AI-powered natural language chatbot** that converts plain English questions into SQL queries and returns answers in clear, readable language. Built with **LangChain**, **Groq's Llama 3.3 70B**, and **Microsoft SQL Server** running on the classic Northwind ERP dataset.

> 🧠 Ask anything about your data — no SQL knowledge needed. The AI handles it all.

Achieved **91% semantic SQL accuracy** across 500+ test queries through systematic prompt engineering and chain-of-thought reasoning.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **Natural Language to SQL** | Ask questions in plain English — AI writes the SQL |
| 🗄️ **MS SQL Server Integration** | Live connection to Microsoft SQL Server backend |
| 🔒 **Read-Only Enforcement** | SELECT-only queries — zero risk of data modification |
| 🌐 **Gradio Web UI** | Clean, instant web interface — no setup for end users |
| ⚡ **Groq Llama 3.3 70B** | Ultra-fast LLM inference via Groq API |
| 🔄 **SQLite Fallback** | Auto demo mode if SQL Server is unavailable |
| 📊 **Plain English Answers** | Results returned as readable sentences, not raw tables |
| 🎯 **91% SQL Accuracy** | Validated across 500+ diverse test queries |

---

## 🔗 Live Demo

<div align="center">

| | Link | Description |
|--|------|-------------|
| 🤗 | [**huggingface.co/spaces/Akshay718/northwind-chatbot**](https://huggingface.co/spaces/Akshay718/northwind-chatbot) | Try the chatbot live — no setup needed |

</div>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     GRADIO WEB UI                        │
│                                                          │
│   User types a natural language question                 │
│   e.g. "Who are the top 5 customers by revenue?"        │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              LANGCHAIN + GROQ LLAMA 3.3 70B             │
│                                                          │
│   Schema-injected context (tables · columns · FK)       │
│   Chain-of-thought SQL generation                        │
│   Read-only SELECT enforcement                           │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│           MICROSOFT SQL SERVER (Northwind DB)            │
│                                                          │
│   SQLAlchemy ORM  →  PyODBC driver  →  SQL Server       │
│   Tables: Customers · Orders · Products · Employees      │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  NATURAL LANGUAGE ANSWER                 │
│   Raw SQL results → Groq LLM → Plain English response   │
└─────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Pipeline

```
  User Types Question (plain English)
         │
         ▼
  ┌──────────────────────────────────┐
  │     Schema Context Injection      │
  │  ├── Table names                 │
  │  ├── Column definitions          │
  │  └── Foreign key relationships   │
  └────────┬─────────────────────────┘
           │
           ▼
  ┌──────────────────────────────────┐
  │     Groq API — SQL Generation    │
  │   Model: llama-3.3-70b           │
  │   ├── Chain-of-thought prompting │
  │   ├── SELECT-only enforcement    │
  │   └── 25+ prompt variations      │
  └────────┬─────────────────────────┘
           │
           ▼
  ┌──────────────────────────────────┐
  │     SQL Server Execution         │
  │   SQLAlchemy → PyODBC → MSSQL   │
  │   Read-only · validated query    │
  └────────┬─────────────────────────┘
           │
           ▼
  ┌──────────────────────────────────┐
  │     Groq API — Answer Generation │
  │   Raw results → plain English    │
  │   Clear · concise · accurate     │
  └────────┬─────────────────────────┘
           │
           ▼
  Answer shown in Gradio UI
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.13 | Core programming language |
| **AI Framework** | LangChain | LLM orchestration and SQL agent |
| **LLM** | Groq llama-3.3-70b-versatile | Natural language to SQL generation |
| **Database** | Microsoft SQL Server | Live ERP backend |
| **Dataset** | Northwind Database | Classic ERP sample data |
| **UI** | Gradio | Web-based chat interface |
| **ORM** | SQLAlchemy | Database abstraction layer |
| **Driver** | PyODBC | SQL Server connection driver |
| **Hosting** | Hugging Face Spaces | Live public demo |

</div>

---

## 📁 Project Structure

```
northwind-chatbot/
├── 📄 chatbot.py          → Main chatbot application
├── 📄 config.py           → Database configuration
├── 📄 requirements.txt    → Python dependencies
├── 📄 instnwnd.sql        → Northwind database setup script
├── 📄 .gitignore          → Git ignore rules
├── 📁 screenshots/        → Output screenshots
└── 📄 README.md           → This file
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Microsoft SQL Server (or SQL Server Express)
- ODBC Driver 17 for SQL Server
- Free Groq API Key → [console.groq.com](https://console.groq.com)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/akshayy718/northwind-chatbot.git
cd northwind-chatbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

**4. Configure SQL Server in `config.py`:**
```python
DATABASE_CONFIG = {
    "server": "YOUR_SERVER_NAME",
    "database": "Northwind",
    "username": "",
    "password": ""
}
```

```bash
# 5. Run the chatbot
python chatbot.py
```

Open → `http://localhost:7860`

---

## 💬 Example Questions

```
💡 Try asking...

"How many customers are there?"
"Show all customers from Germany"
"What are the top 5 most expensive products?"
"How many orders were placed in 1997?"
"What is the total revenue from all orders?"
"Who are the top 10 customers by number of orders?"
"Show all products in the Beverages category"
"Which employee has handled the most orders?"
"List all suppliers based in the USA"
"What is the average order value per customer?"
```

---

## 📊 Performance

| Metric | Result |
|--------|--------|
| **Semantic SQL Accuracy** | 91% across 500+ test queries |
| **Complex Query Accuracy** | Improved from 76% → 89% via prompt engineering |
| **Query Latency** | Reduced from 2.3s → 0.8s after index optimization |
| **Prompt Variations Tested** | 25+ systematic variations |
| **Safety** | 0 destructive queries — SELECT-only enforced |

---

## 🔮 Future Improvements

- [ ] **Multi-database support** — PostgreSQL · MySQL · SQLite
- [ ] **Chat history** — multi-turn conversation memory
- [ ] **Query explainer** — show generated SQL to the user
- [ ] **Voice input** — speak your question instead of typing
- [ ] **Export results** — download answers as CSV
- [ ] **Custom datasets** — plug in any SQL database

---

## 👨‍💻 Author

<div align="center">

**Akshay Santhosh** — AI/ML Engineer · LLM & SQL Agent Builder

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Akshay%20Santhosh-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/akshay-santhosh-435499208/)
[![GitHub](https://img.shields.io/badge/GitHub-akshayy718-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/akshayy718)
[![Email](https://img.shields.io/badge/Gmail-akshaysanthosh718-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:akshaysanthosh718@gmail.com)

</div>

---

<div align="center">

*Built with ❤️ using Python · LangChain · Groq AI · Gradio · Microsoft SQL Server*

<img src="https://capsule-render.vercel.app/api?type=waving&color=0,FFD700,FFA500,FF7C00&height=130&section=footer&animation=fadeIn" width="100%"/>

</div>
