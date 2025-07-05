# 🤖 Complaint Assistant Chatbot

A smart, Gemini-powered chatbot that lets users:
- 📝 Register a complaint
- 🔍 Fetch complaint status by ID
- ❓ Ask FAQ-style questions answered via RAG

---

## 🧠 Architecture Overview

```mermaid
graph LR
    U[User] --> S[Streamlit Chat UI\\n(chat_app.py)]
    S --> C[Intent Classifier\\n(Gemini via LangChain)]
    C --> R[RAG (FAQs)\\nLangChain + PDF]
    C --> F[Flask API\\n(app.py)]
    F --> DB[SQLite DB\\n(complaints.db)]
    R --> S
    F --> S
```
