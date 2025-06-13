import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI

# --- API Key (fix here directly) ---
GOOGLE_API_KEY = "AIzaSyAPSM-tjDDFZcCploLoXiJ8MkjxAA5ukwk"  # Replace with your actual API key

# --- Streamlit UI Setup ---
st.set_page_config(page_title="English to French Translator", layout="centered")
st.title("🌍 English to French Translator")
st.markdown("Translate any English sentence into French using Gemini + LangChain.")

# --- Gemini Model Setup ---
try:
    llm = ChatGoogleGenerativeAI(
    model="models/chat-bison-001",  # Free-tier supported model
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3
)
except Exception as e:
    st.error(f"❌ Failed to load Gemini model: {e}")
    st.stop()

# --- Prompt Template ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates English to French."),
    ("user", "Translate this sentence: {input}")
])

# --- Chain using Runnable ---
chain: Runnable = prompt | llm

# --- Input UI ---
user_input = st.text_input("✍️ Enter English sentence:")
if st.button("Translate to French"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a sentence.")
    else:
        try:
            with st.spinner("Translating..."):
                response = chain.invoke({"input": user_input})
                translated = response.content
                st.success("✅ Translation successful!")
                st.text_area("🇫🇷 French Translation:", translated, height=120)
        except Exception as e:
            st.error(f"❌ Error during translation: {e}")
