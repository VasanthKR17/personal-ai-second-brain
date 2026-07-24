import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

load_dotenv()

st.set_page_config(
    page_title="Personal AI Second Brain",
    page_icon="🧠",
    layout="wide",
)

# ---------- CUSTOM STYLING ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a855f7, #ec4899, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-top: 1rem;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #b8b8d1;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .chat-bubble-user {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .chat-bubble-ai {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        color: #e5e5f7;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        border: 1px solid rgba(168, 85, 247, 0.3);
    }
    .note-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 3px solid #a855f7;
        padding: 10px 14px;
        border-radius: 8px;
        margin: 6px 0;
        color: #d1d1e9;
        font-size: 0.9rem;
    }
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95);
        border-right: 1px solid rgba(168, 85, 247, 0.2);
    }
    div[data-testid="stTextInput"] input {
        border-radius: 12px;
        border: 1px solid rgba(168, 85, 247, 0.4);
    }
    .stButton button {
        background: linear-gradient(90deg, #a855f7, #ec4899);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: transform 0.2s;
    }
    .stButton button:hover {
        transform: scale(1.03);
    }
</style>
""", unsafe_allow_html=True)

# ---------- SETUP MODELS (cached so it doesn't reload every interaction) ----------
@st.cache_resource
def load_models():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    db = Chroma(
        persist_directory="data",
        embedding_function=embeddings
    )
    return embeddings, llm, db

embeddings, llm, db = load_models()

# ---------- SESSION STATE ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- HEADER ----------
st.markdown('<p class="main-title">🧠 Personal AI Second Brain</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your notes, made searchable and conversational.</p>', unsafe_allow_html=True)

# ---------- SIDEBAR: SAVE NOTES ----------
with st.sidebar:
    st.markdown("### 📝 Save a New Note")
    new_note = st.text_area("What do you want to remember?", height=100, label_visibility="collapsed", placeholder="Type a note here...")
    if st.button("💾 Save Note", use_container_width=True):
        if new_note.strip():
            with open("my_notes.txt", "a") as f:
                f.write(new_note.strip() + "\n")
            db.add_texts([new_note.strip()])
            st.success("Saved and remembered! ✅")
        else:
            st.warning("Please type something first.")

    st.markdown("---")
    st.markdown("### 📄 Upload a Document")
    uploaded_file = st.file_uploader("Upload a PDF or text file", type=["pdf", "txt"], label_visibility="collapsed")

    if uploaded_file is not None:
        if st.button("📥 Ingest Document", use_container_width=True):
            with st.spinner("Reading and processing document..."):
                if uploaded_file.name.endswith(".pdf"):
                    reader = PdfReader(uploaded_file)
                    full_text = ""
                    for page in reader.pages:
                        full_text += page.extract_text() + "\n"
                else:
                    full_text = uploaded_file.read().decode("utf-8")

                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=50
                )
                chunks = splitter.split_text(full_text)

                db.add_texts(chunks)

                with open("my_notes.txt", "a") as f:
                    f.write(f"[Document: {uploaded_file.name}] {len(chunks)} sections ingested\n")

            st.success(f"✅ Ingested {len(chunks)} chunks from '{uploaded_file.name}'!")

    st.markdown("---")
    st.markdown("### 📚 Recent Notes")
    try:
        with open("my_notes.txt", "r") as f:
            notes = [n.strip() for n in f.readlines() if n.strip()]
        for note in notes[-5:][::-1]:
            st.markdown(f'<div class="note-card">{note}</div>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.info("No notes yet — save your first one above!")

# ---------- MAIN CHAT AREA ----------
st.markdown("### 💬 Ask Your Second Brain")

for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="chat-bubble-user">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-ai">{message}</div>', unsafe_allow_html=True)

question = st.chat_input("Ask something about your notes...")

if question:
    st.session_state.chat_history.append(("user", question))

    with st.spinner("🔎 Searching your memory..."):
        results = db.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in results])

        prompt = f"""Answer the question using only the notes below.

Notes:
{context}

Question: {question}
"""
        response = llm.invoke(prompt)
        answer = ""
        for block in response.content_blocks:
            if block["type"] == "text":
                answer += block["text"]

    st.session_state.chat_history.append(("ai", answer))
    st.rerun()