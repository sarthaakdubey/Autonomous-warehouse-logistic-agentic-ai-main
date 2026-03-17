import streamlit as st
import requests
from datetime import datetime

# ---------------- CONFIG ----------------
API_URL = "http://127.0.0.1:8000/research"

st.set_page_config(
    page_title="Warehouse AI Agent",
    page_icon="📦",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Controls")

mode = st.sidebar.radio(
    "Query Mode",
    ["Auto (Recommended)", "Dataset Only", "Research Only"]
)

show_sources = st.sidebar.checkbox("Show Sources", True)
show_reasoning = st.sidebar.checkbox("Show Agent Reasoning", True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Example Questions")

examples = [
    "order 1003 details",
    "which warehouse has most delays",
    "why orders delayed",
    "how to improve warehouse operations",
    "latest warehouse automation technologies"
]

for q in examples:
    if st.sidebar.button(q):
        st.session_state["preset"] = q

# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("📦 Autonomous Logistics Research Agent")
st.caption("Multi-Agent AI powered by CrewAI + RAG + Tavily")

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ----------------
user_input = st.chat_input("Ask about warehouse operations...")

# preset click support
if "preset" in st.session_state:
    user_input = st.session_state["preset"]
    del st.session_state["preset"]


# ---------------- HELPER FUNCTION ----------------
def format_result(result):
    if isinstance(result, dict):
        formatted = ""
        for key, value in result.items():
            formatted += f"### {key.replace('_', ' ').title()}\n{value}\n\n"
        return formatted
    elif isinstance(result, str):
        return result.replace("\\n", "\n").strip()
    return "❌ Invalid result format"


# ---------------- REQUEST ----------------
if user_input:

    # store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("🤖 Agents analyzing warehouse data..."):

            try:
                response = requests.post(
                    API_URL,
                    json={"question": user_input},
                    timeout=120
                )

                if response.status_code == 200:
                    try:
                        data = response.json()
                    except Exception:
                        result = f"❌ Invalid JSON response:\n{response.text}"
                    else:
                        raw_result = data.get("result")
                        error = data.get("error")

                        if raw_result:
                            result = format_result(raw_result)

                            # Show reasoning
                            if show_reasoning and "status" in data:
                                result += "\n---\n### 🧠 Agent Execution\n"
                                result += "\n".join([f"- {s}" for s in data["status"]])

                        elif error:
                            result = f"❌ {error}"

                        else:
                            result = f"❌ Unexpected response:\n{data}"

                else:
                    result = f"❌ Server Error ({response.status_code}):\n{response.text}"

            except requests.exceptions.ConnectionError:
                result = "❌ Cannot connect to backend. Make sure FastAPI is running."

            except requests.exceptions.Timeout:
                result = "❌ Request timed out. Backend is taking too long."

            except Exception as e:
                result = f"❌ Unexpected Error:\n{str(e)}"

        st.markdown(result)

    # save assistant response
    st.session_state.messages.append({"role": "assistant", "content": result})


# ---------------- DOWNLOAD CHAT ----------------
if st.session_state.messages:
    full_chat = "\n\n".join(
        [f"{m['role'].upper()}:\n{m['content']}" for m in st.session_state.messages]
    )

    st.download_button(
        "⬇️ Download Conversation",
        full_chat,
        file_name=f"warehouse_report_{datetime.now().strftime('%H%M%S')}.txt"
    )