# rag_bot.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.language_models import BaseLanguageModel
from langchain.llms.base import LLM
from typing import Optional, List, Any

# Load .env for Gemini key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom LangChain-compatible Gemini wrapper
class GeminiLLM(LLM):
    model: Any = genai.GenerativeModel("gemini-1.5-flash")


    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.model.generate_content(prompt)
        return response.text

    @property
    def _llm_type(self) -> str:
        return "gemini"
    
def classify_user_intent(message):
    prompt = (
        "You are a smart classifier that receives a user message and returns one of the following intents ONLY:"
        "- greet → for greetings like 'hi', 'hello', 'hey'"
        "- thanks → for gratitude or closing like 'thank you', 'bye'"
        "- register → when the user wants to file a new complaint, e.g., 'I want to complain', 'report issue'"
        "- fetch → when the user wants to check complaint status, e.g., 'check my complaint', 'what is my complaint status'"
        "- faq → when the user is asking about support process, response time, contact info, etc."
        "Return ONLY the matching intent with no extra explanation."
        f"\nMessage: {message}\nIntent:"
    )
    return GeminiLLM()._call(prompt).strip().lower()

def create_qa_chain():
    loader = PyPDFLoader("knowledge_base/faqs.pdf")
    docs = loader.load()

    # FREE embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)
    retriever = db.as_retriever()

    qa = RetrievalQA.from_chain_type(
        llm=GeminiLLM(),
        retriever=retriever
    )
    return qa
