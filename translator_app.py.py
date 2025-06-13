import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

# --- SET YOUR GEMINI API KEY HERE ---
GOOGLE_API_KEY = "AIzaSyAPSM-tjDDFZcCploLoXiJ8MkjxAA5ukwk"  # ⬅️ Replace this with your actual key

# --- Page Setup ---
st.set_page_config(page_title="English to French Translator", layout="centered")
st.title("🌐 English ➡️ French Translator")
st.markdown("Translate any English sentence into French using Google Gemini + LangChain")

# --- Initialize Gemini Model ---
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",  # ✅ Correct model name
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    )
except Exception as e:
    st.error(f"❌ Failed to load Gemini model: {e}")
    st.stop()

# --- Prompt Template ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional translator. Translate the given English text to French."),
    ("user", "{input_text}")
])

# --- Build the Chain using | operator ---
chain: Runnable = prompt | llm

# --- User Input ---
user_input = st.text_input("📝 Enter English sentence:", placeholder="e.g. Good morning, how are you?")

# --- Translate Button ---
if st.button("Translate to French"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a sentence to translate.")
    else:
        try:
            # Invoke the chain
            response = chain.invoke({"input_text": user_input})
            french_translation = response.content.strip()

            # Display result
            st.success("✅ Successfully translated!")
            st.markdown(f"**🇫🇷 French:**\n> {french_translation}")

        except Exception as e:
            st.error(f"❌ Error during translation: {str(e)}")
