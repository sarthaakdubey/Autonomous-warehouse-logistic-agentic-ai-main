import streamlit as st
import requests
from datetime import datetime

# ---------------- CONFIG ----------------
API_URL = "http://127.0.0.1:8000/research"
UPLOAD_API = "http://127.0.0.1:8000/upload"

st.set_page_config(
    page_title="Warehouse AI Agent",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Root Variables ─── */
:root {
    --bg-primary: #0a0c10;
    --bg-secondary: #111318;
    --bg-card: #161920;
    --bg-hover: #1c2029;
    --border: #252a35;
    --border-active: #3a4255;
    --accent: #f0c040;
    --accent-dim: rgba(240, 192, 64, 0.12);
    --accent-glow: rgba(240, 192, 64, 0.25);
    --text-primary: #e8eaf0;
    --text-secondary: #8892a4;
    --text-muted: #4a5568;
    --green: #34d399;
    --red: #f87171;
    --blue: #60a5fa;
    --purple: #a78bfa;
    --radius: 10px;
}

/* ─── Global Reset ─── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ─── Hide Streamlit Branding ─── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1100px !important;
}

/* ─── Sidebar ─── */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1.2rem !important;
}
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.8rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid var(--border);
}
.sidebar-brand .icon {
    font-size: 1.5rem;
    background: var(--accent-dim);
    border: 1px solid var(--accent-glow);
    border-radius: 8px;
    width: 40px; height: 40px;
    display: flex; align-items: center; justify-content: center;
}
.sidebar-brand .label {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.1em;
    line-height: 1.2;
    text-transform: uppercase;
}
.sidebar-brand .sublabel {
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 0.05em;
}
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin: 1.2rem 0 0.6rem 0;
}

/* ─── Radio Buttons ─── */
.stRadio > label {
    font-size: 0.78rem !important;
    color: var(--text-secondary) !important;
    margin-bottom: 0.3rem !important;
}
.stRadio [data-testid="stWidgetLabel"] {
    display: none !important;
}
.stRadio div[role="radiogroup"] {
    gap: 0.3rem !important;
}
.stRadio div[role="radiogroup"] label {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 0.5rem 0.8rem !important;
    font-size: 0.78rem !important;
    color: var(--text-secondary) !important;
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
}
.stRadio div[role="radiogroup"] label:hover {
    border-color: var(--border-active) !important;
    background: var(--bg-hover) !important;
    color: var(--text-primary) !important;
}

/* ─── Checkboxes ─── */
.stCheckbox label {
    font-size: 0.78rem !important;
    color: var(--text-secondary) !important;
}

/* ─── Example Buttons ─── */
.stButton > button {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-size: 0.72rem !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.35rem 0.7rem !important;
    text-align: left !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
    margin-bottom: 0.25rem !important;
}
.stButton > button:hover {
    background: var(--accent-dim) !important;
    border-color: var(--accent-glow) !important;
    color: var(--accent) !important;
    transform: translateX(2px) !important;
}

/* ─── File Uploader ─── */
.stFileUploader {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border-active) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
}
.stFileUploader label {
    font-size: 0.78rem !important;
    color: var(--text-secondary) !important;
}
[data-testid="stFileUploadDropzone"] {
    background: transparent !important;
    border: none !important;
}

/* ─── Hero Header ─── */
.hero-header {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 300px; height: 300px;
    background: radial-gradient(circle at top right, rgba(240, 192, 64, 0.06), transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--accent-dim);
    border: 1px solid var(--accent-glow);
    border-radius: 20px;
    padding: 4px 12px;
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-badge .dot {
    width: 6px; height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin: 0 0 0.6rem 0;
}
.hero-title span {
    color: var(--accent);
}
.hero-subtitle {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
}
.stat-row {
    display: flex;
    gap: 1.2rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.stat-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.4rem 0.8rem;
    font-size: 0.72rem;
    color: var(--text-secondary);
}
.stat-pill .dot-green { width: 6px; height: 6px; background: var(--green); border-radius: 50%; }
.stat-pill .dot-blue { width: 6px; height: 6px; background: var(--blue); border-radius: 50%; }
.stat-pill .dot-purple { width: 6px; height: 6px; background: var(--purple); border-radius: 50%; }

/* ─── Upload Panel ─── */
.upload-panel {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
}
.panel-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.8rem;
}

/* ─── Chat Container ─── */
.chat-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
    min-height: 100px;
}

/* ─── Chat Messages ─── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.5rem 0 !important;
}
[data-testid="stChatMessage"][data-testid*="user"] .stMarkdown {
    background: var(--bg-secondary) !important;
}

/* User bubble */
[data-testid="stChatMessageContent"] {
    border-radius: var(--radius) !important;
}

/* ─── Chat Input ─── */
[data-testid="stChatInput"] {
    border: 1px solid var(--border) !important;
    background: var(--bg-card) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent-glow) !important;
    box-shadow: 0 0 0 3px rgba(240, 192, 64, 0.08) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
}

/* ─── Alert / Info boxes ─── */
.stAlert {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-size: 0.82rem !important;
    color: var(--text-secondary) !important;
}
.stAlert [data-testid="stMarkdownContainer"] {
    color: var(--text-secondary) !important;
}

/* ─── Success / Error ─── */
.element-container .stSuccess {
    background: rgba(52, 211, 153, 0.08) !important;
    border: 1px solid rgba(52, 211, 153, 0.2) !important;
    border-radius: var(--radius) !important;
    color: var(--green) !important;
}
.element-container .stError {
    background: rgba(248, 113, 113, 0.08) !important;
    border: 1px solid rgba(248, 113, 113, 0.2) !important;
    border-radius: var(--radius) !important;
    color: var(--red) !important;
}

/* ─── Spinner ─── */
.stSpinner > div {
    border-top-color: var(--accent) !important;
}

/* ─── Download Button ─── */
.stDownloadButton > button {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-size: 0.78rem !important;
    font-family: 'Space Mono', monospace !important;
    padding: 0.4rem 1rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    border-color: var(--accent-glow) !important;
    color: var(--accent) !important;
    background: var(--accent-dim) !important;
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-active); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ─── Separator ─── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.2rem 0 !important;
}

/* Mode tag chips */
.mode-tag {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.65rem;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.06em;
    margin-bottom: 0.5rem;
}
.mode-rag    { background: rgba(96,165,250,0.12); color: #60a5fa; border: 1px solid rgba(96,165,250,0.2); }
.mode-dataset{ background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.2); }
.mode-research{ background: rgba(167,139,250,0.12); color: #a78bfa; border: 1px solid rgba(167,139,250,0.2); }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="icon">📦</div>
        <div>
            <div class="label">Warehouse AI</div>
            <div class="sublabel">Multi-Agent System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Query Mode</div>', unsafe_allow_html=True)
    mode = st.radio(
        "Query Mode",
        ["Auto (Recommended)", "Dataset Only", "Research Only"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label">Display</div>', unsafe_allow_html=True)
    show_sources = st.checkbox("Show Sources", True)
    show_reasoning = st.checkbox("Show Agent Reasoning", True)

    st.markdown("---")
    st.markdown('<div class="section-label">Quick Queries</div>', unsafe_allow_html=True)

    examples = [
        "📋  order 1003 details",
        "🏭  warehouse with most delays",
        "🔍  why are orders delayed",
        "📈  improve warehouse operations",
        "🤖  latest automation technologies",
        "📄  delays from document",
    ]
    raw_examples = [
        "order 1003 details",
        "which warehouse has most delays",
        "why orders delayed",
        "how to improve warehouse operations",
        "latest warehouse automation technologies",
        "according to the document what are delays",
    ]

    for label, raw in zip(examples, raw_examples):
        if st.button(label, key=f"ex_{raw[:10]}"):
            st.session_state["preset"] = raw

    st.markdown("---")
    st.markdown('<div class="section-label">Upload Documents</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "PDF or CSV",
        type=["pdf", "csv"],
        label_visibility="collapsed",
        key="sidebar_upload"
    )

    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        try:
            with st.spinner("Uploading..."):
                res = requests.post(UPLOAD_API, files=files)
            if res.status_code == 200:
                st.success(f"✅ {uploaded_file.name} uploaded")
            else:
                st.error(f"Upload failed: {res.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ---------------- HERO HEADER ----------------
st.markdown("""
<div class="hero-header">
    <div class="hero-badge">
        <span class="dot"></span>
        System Active
    </div>
    <div class="hero-title">Autonomous <span>Logistics</span> Agent</div>
    <p class="hero-subtitle">
        Query warehouse data, upload logistics documents, and get AI-powered insights
        from your operations — all in one place.
    </p>
    <div class="stat-row">
        <div class="stat-pill"><span class="dot-green"></span>CrewAI Multi-Agent</div>
        <div class="stat-pill"><span class="dot-blue"></span>RAG Pipeline</div>
        <div class="stat-pill"><span class="dot-purple"></span>Tavily Web Search</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- MAIN UPLOAD ----------------
st.markdown('<div class="panel-title">📂 Upload Document</div>', unsafe_allow_html=True)
with st.container():
    main_upload = st.file_uploader(
        "Drag & drop PDF or CSV here",
        type=["pdf", "csv"],
        key="main_upload",
        label_visibility="collapsed"
    )

    if main_upload is not None:
        files = {"file": (main_upload.name, main_upload.getvalue())}
        try:
            with st.spinner(f"Uploading {main_upload.name}..."):
                res = requests.post(UPLOAD_API, files=files)
            if res.status_code == 200:
                st.success(f"✅ **{main_upload.name}** is ready for queries.")
            else:
                st.error(f"❌ Upload failed ({res.status_code})")
        except Exception as e:
            st.error(f"❌ {str(e)}")

st.markdown("---")
st.markdown('<div class="panel-title">💬 Conversation</div>', unsafe_allow_html=True)

# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# ---------------- INPUT ----------------
user_input = st.chat_input("Ask about your warehouse data, documents, or operations...")

if "preset" in st.session_state:
    user_input = st.session_state["preset"]
    del st.session_state["preset"]

# ---------------- HELPER ----------------
def format_result(result, mode_tag=""):
    tag_html = ""
    if mode_tag == "rag":
        tag_html = '<span class="mode-tag mode-rag">📄 Document RAG</span><br>'
    elif mode_tag == "dataset":
        tag_html = '<span class="mode-tag mode-dataset">📊 Dataset</span><br>'
    elif mode_tag == "research":
        tag_html = '<span class="mode-tag mode-research">🧠 AI Research</span><br>'

    if isinstance(result, dict):
        formatted = tag_html
        for key, value in result.items():
            formatted += f"**{key.replace('_', ' ').title()}**\n\n{value}\n\n"
        return formatted
    elif isinstance(result, str):
        return tag_html + result.replace("\\n", "\n").strip()
    return "❌ Invalid result format"

# ---------------- REQUEST ----------------
if user_input:
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
                        resp_mode = data.get("mode", "unknown")

                        if raw_result:
                            result = format_result(raw_result, resp_mode)

                            if show_reasoning and "status" in data:
                                result += "\n\n---\n**🧠 Agent Execution Log**\n\n"
                                result += "\n".join([f"- `{s}`" for s in data["status"]])
                        elif error:
                            result = f"❌ {error}"
                        else:
                            result = f"❌ Unexpected response:\n```json\n{data}\n```"
                else:
                    result = f"❌ Server Error `{response.status_code}`\n\n{response.text}"

            except requests.exceptions.ConnectionError:
                result = "❌ **Cannot connect to backend.** Make sure the API server is running on `localhost:8000`."
            except requests.exceptions.Timeout:
                result = "❌ **Request timed out.** The agents took too long to respond."
            except Exception as e:
                result = f"❌ **Error:** {str(e)}"

        st.markdown(result, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": result})

# ---------------- DOWNLOAD ----------------
if st.session_state.messages:
    st.markdown("---")
    full_chat = "\n\n".join(
        [f"{m['role'].upper()}:\n{m['content']}" for m in st.session_state.messages]
    )
    col1, col2 = st.columns([1, 5])
    with col1:
        st.download_button(
            "⬇️ Export Chat",
            full_chat,
            file_name=f"warehouse_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
