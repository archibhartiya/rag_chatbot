# 🤖 Complaint Assistant Chatbot

A smart, Gemini-powered chatbot that lets users:

- 📝 Register a complaint  
- 🔍 Fetch complaint status by ID  
- ❓ Ask FAQ-style questions answered via RAG  

---

## 🔄 Flow Description

**1. User Interaction:**  
Users interact through the friendly Streamlit chat interface.

**2. Intent Classification:**  
Gemini (via LangChain) classifies input as:
- `register`
- `fetch`
- `faq`
- `greet`
- `thanks`

**3. Routing Logic:**
- 🤖 FAQ queries → Routed to the **RAG engine** (PDF-based)
- 📝 Complaint intents → Routed to the **Flask API**

**4. Data Handling:**
- RAG answers are derived from a **PDF knowledge base**
- Complaints are stored and retrieved from **SQLite database**

**5. Response Delivery:**  
All results (answers or status) are returned via the Streamlit UI.

---

## 🗂️ Folder Structure

```
rag_chatbot/
├── chat_app.py              # Streamlit chatbot UI
├── app.py                   # Flask backend API
├── rag_bot.py               # Gemini + LangChain logic
├── requirements.txt         # Python dependencies
├── .env.example             # Placeholder for Gemini API key
├── complaints.db            # Auto-generated SQLite DB
├── knowledge_base/faqs.pdf  # RAG source document
└── README.md
```

---

## 🚀 Setup & Run Locally

### ✅ 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/rag_chatbot.git
cd rag_chatbot
```

### ✅ 2. Setup Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# OR
source venv/bin/activate     # macOS/Linux
```

### ✅ 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### ✅ 4. Add Your Gemini API Key

Create a `.env` file with the following:

```env
GOOGLE_API_KEY=your-gemini-api-key
```

> ⚠️ **Important**: Never commit this `.env` file to GitHub!

### ✅ 5. Run the App

#### Backend (Flask API):

```bash
python app.py
```

#### Frontend (Streamlit chatbot):

```bash
streamlit run chat_app.py
```

---

## 💬 Features

- 🤖 Detects user intent (`register`, `fetch`, `faq`, `greet`, `thanks`)
- 📝 Handles full complaint registration process with validation
- 📄 Provides FAQ support using Gemini + LangChain RAG (PDF-based)
- 💬 Maintains natural, flowing conversation with fallback support

---

## 🙌 Contributing

Pull requests are welcome!  
Feel free to fork this repo, improve features, or adapt it to your own RAG-based use cases. 🚀
