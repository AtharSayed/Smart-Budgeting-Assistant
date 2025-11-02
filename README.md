# Smart-Budgeting-Assistant
A context-aware, LLM-powered financial assistant that helps you track expenses, analyze spending, and make smarter budgeting decisions — all through natural language
 
## 🧭 Project Structure

```bash
smart-budget-assistant/
│
├── app/                          # Core application
│   ├── __init__.py
│   ├── main.py                   # FastAPI entrypoint
│   ├── database.py               # DB engine + session
│   ├── models.py                 # SQLModel: Expense, Category, UserProfile
│   ├── categorizer.py            # Auto-categorize with 50/30/20 awareness
│   ├── context_manager.py        # BudgetContext: 50/30/20, spending, balance
│   └── llm_handler.py            # LLM integration (Mistral via Ollama)
│
├── scripts/                      # Dev & data tools
│   ├── generate_synthetic_data.py
│   └── ingest_csv.py             # Recreate DB + insert with balance + 50/30/20 budgets
│
├── static/                       # Frontend assets
│   ├── index.html                # Chat UI + Chart
│   └── style.css                 # Styled UI
│
├── generated/                    # Auto-generated (git-ignore)
│   └── sample_expenses_5months.csv
│
├── data/                         # Runtime DB (git-ignore)
│   └── budget.db                 # SQLite file
│
├── tests/                        # Unit & integration tests
│   ├── __init__.py
│   ├── test_categorizer.py
│   ├── test_context.py
│   └── test_llm.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```

 