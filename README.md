# 🤖 Complaint Assistant Chatbot

A smart, Gemini-powered chatbot that lets users:
- 📝 Register a complaint
- 🔍 Fetch complaint status by ID
- ❓ Ask FAQ-style questions answered via RAG

---

## 🧠 Architecture Overview

```mermaid
graph LR
    U[User]
    S[Streamlit Chat UI (chat_app.py)]
    C[Intent Classifier (Gemini + LangChain)]
    R[RAG Engine (FAQs from PDF)]
    F[Flask API (app.py)]
    DB[SQLite DB (complaints.db)]

    U --> S
    S --> C
    C --> R
    C --> F
    F --> DB
    R --> S
    F --> S
```
