import streamlit as st
import requests
import re
from rag_bot import create_qa_chain, classify_user_intent

# Load the RAG chain once
qa = create_qa_chain()
API_URL = "http://localhost:5000/complaints"

if 'stage' not in st.session_state:
    st.session_state.stage = 'chat'
    st.session_state.user_inputs = {}
    st.session_state.chat_history = []
    st.session_state.last_complaint_id = None

st.title("🤖 Complaint Assistant Chatbot")

user_query = st.chat_input("Type your message here...")

def handle_user_input(user_query):
    st.session_state.chat_history.append(("user", user_query))

    # Keep intent only for new flows, ignore reclassification if in the middle of a flow
    if st.session_state.stage in ['name', 'phone', 'email', 'details']:
        intent = 'register'
    else:
        intent = classify_user_intent(user_query)
    print(f"Intent: {intent}")

    if intent == 'greet':
        st.session_state.stage = 'chat'
        st.session_state.user_inputs = {}
        st.session_state.last_complaint_id = None
        st.session_state.chat_history.append(("bot", "👋 Hi there! Let me know if you'd like to file a complaint, check one, or ask a question."))
        return

    if intent == 'thanks':
        st.session_state.chat_history.append(("bot", "😊 You're welcome! If anything else comes up, just type 'hi' to begin again."))
        return

    if intent == 'register':
        if st.session_state.stage == 'chat':
            st.session_state.stage = 'name'
            st.session_state.chat_history.append(("bot", f"I can help with that. Could you please tell me your name so we can get started?"))
            return

        if st.session_state.stage == 'name':
            if not user_query.strip():
                st.session_state.chat_history.append(("bot", "❗ Please provide a valid name to proceed."))
                return
            st.session_state.user_inputs["name"] = user_query
            st.session_state.stage = 'phone'
            st.session_state.chat_history.append(("bot", f"Thanks {user_query.split()[0]}, and what's the best number to reach you at?"))
            return

        if st.session_state.stage == 'phone':
            if not re.fullmatch(r'\d{10}', user_query.strip()):
                st.session_state.chat_history.append(("bot", "📱 Please enter a valid 10-digit phone number."))
                return
            st.session_state.user_inputs["phone_number"] = user_query
            st.session_state.stage = 'email'
            st.session_state.chat_history.append(("bot", "Got it. Can you also provide your email so we can contact you if needed?"))
            return

        if st.session_state.stage == 'email':
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+", user_query.strip()):
                st.session_state.chat_history.append(("bot", "✉️ That doesn't look like a valid email. Please enter a valid email address."))
                return
            st.session_state.user_inputs["email"] = user_query
            st.session_state.stage = 'details'
            st.session_state.chat_history.append(("bot", "Almost done! Please describe the issue you're facing so I can log it properly."))
            return

        if st.session_state.stage == 'details':
            if len(user_query.strip()) < 10:
                st.session_state.chat_history.append(("bot", "📝 Please provide a few more details so we can understand your complaint better."))
                return
            st.session_state.user_inputs["complaint_details"] = user_query
            try:
                response = requests.post(API_URL, json=st.session_state.user_inputs)
                if response.status_code == 200:
                    cid = response.json().get("complaint_id")
                    st.session_state.last_complaint_id = cid
                    st.session_state.chat_history.append(("bot", f"✅ I've registered your complaint! Your complaint ID is **{cid}**. Keep this safe in case you want to check the status later."))
                else:
                    st.session_state.chat_history.append(("bot", "❌ Hmm, something went wrong while registering your complaint."))
            except Exception as e:
                st.session_state.chat_history.append(("bot", f"❌ Error: {str(e)}"))
            st.session_state.stage = 'chat'
            st.session_state.user_inputs = {}
            return

    elif intent == 'fetch':
        possible_ids = re.findall(r'\b([a-zA-Z0-9]{6,})\b', user_query)
        for cid in possible_ids:
            try:
                response = requests.get(f"{API_URL}/{cid}")
                if response.status_code == 200:
                    data = response.json()
                    reply = f"""
**📄 Complaint Details**
- **ID:** {data['complaint_id']}
- **Name:** {data['name']}
- **Phone:** {data['phone_number']}
- **Email:** {data['email']}
- **Issue:** {data['complaint_details']}
- **Filed On:** {data['created_at']}
- **Status:** {data.get('status', 'Pending')}"""
                    st.session_state.chat_history.append(("bot", reply))
                    return
            except Exception as e:
                st.session_state.chat_history.append(("bot", f"❌ Error retrieving complaint: {str(e)}"))
                return
        st.session_state.chat_history.append(("bot", "Sure! Please share your complaint ID so I can look it up for you."))
        return

    elif intent == 'faq':
        try:
            response = qa.run(user_query)
            if response:
                st.session_state.chat_history.append(("bot", response))
            else:
                st.session_state.chat_history.append(("bot", "🤖 I couldn't find that in our support info. Could you try rephrasing?"))
        except Exception as e:
            st.session_state.chat_history.append(("bot", f"⚠️ RAG error: {str(e)}"))
        return

    st.session_state.chat_history.append(("bot", "🤖 I'm not sure how to respond to that. You can say 'hi' to start over or ask a question."))

if user_query:
    handle_user_input(user_query)

for sender, msg in st.session_state.chat_history:
    with st.chat_message("user" if sender == "user" else "assistant"):
        st.write(msg)