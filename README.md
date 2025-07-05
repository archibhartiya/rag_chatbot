# 🤖 Complaint Assistant Chatbot

A smart, Gemini-powered chatbot that lets users:
- 📝 Register a complaint
- 🔍 Fetch complaint status by ID
- ❓ Ask FAQ-style questions answered via RAG

---

## 🧠 Architecture Overview

```mermaid
graph LR
    U[User] --> S[Streamlit Chat UI<br/>(chat_app.py)]
    S --> C[Intent Classifier<br/>(Gemini via LangChain)]
    C --> R[RAG (FAQs)<br/>LangChain + PDF]
    C --> F[Flask API<br/>(app.py)]
    F --> DB[SQLite DB<br/>(complaints.db)]
    R --> S
    F --> S
