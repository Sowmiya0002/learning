import streamlit as st
import requests

# -----------------------------
# Configuration
# -----------------------------
WEBHOOK_URL = "https://your-n8n-instance.com/webhook/meeting-actions"  # Replace with your actual n8n webhook URL

# Dummy credentials for login (you can expand this securely later)
USERS = {
    "john": "password123",
    "emma": "securepass",
    "admin": "admin123"
}

# -----------------------------
# Session State Setup
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# -----------------------------
# Login Function
# -----------------------------
def login(username, password):
    if username in USERS and USERS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
    else:
        st.error("Invalid username or password.")

# -----------------------------
# Logout Function
# -----------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""

# -----------------------------
# Main App
# -----------------------------
st.set_page_config(page_title="Employee Portal", layout="centered")

st.title("🔐 Secure Employee Portal")

# --- Login Page ---
if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login(username, password)

# --- Portal Page ---
else:
    st.success(f"Welcome, {st.session_state.username}!")
    
    st.subheader("📋 Submit Meeting Action Items")
    with st.form("action_form"):
        meeting_date = st.date_input("Meeting Date")
        action_item = st.text_area("Action Item")
        assigned_to = st.text_input("Assigned To")
        email = st.text_input("Email")  # ✅ New email input field
        due_date = st.date_input("Due Date")
        submit = st.form_submit_button("Submit")

    if submit:
        data = {
            "username": st.session_state.username,
            "meeting_date": str(meeting_date),
            "action_item": action_item,
            "assigned_to": assigned_to,
            "email": email,  # ✅ Added to the POST data
            "due_date": str(due_date)
        }
        try:
            response = requests.post(WEBHOOK_URL, json=data)
            if response.status_code == 200:
                st.success("Action item submitted successfully!")
            else:
                st.error(f"Failed to submit. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")

    # Logout Button
    if st.button("Logout"):
        logout()
        st.experimental_rerun()
