import os
import tempfile
import uuid
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# ----------------------------- Page setup -----------------------------
# Keep your logo at: <project folder>/img/documind.png
BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "img" / "documind.png"
PAGE_ICON = str(LOGO_PATH) if LOGO_PATH.is_file() else "📄"

st.set_page_config(
    page_title="DocuMind | RAG Chat",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Glass UI CSS ---------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --glass: rgba(255,255,255,.075);
        --glass-border: rgba(255,255,255,.17);
        --muted: #b9c7e8;
    }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background:
          radial-gradient(ellipse at 10% 10%, rgba(116, 65, 255, .36), transparent 35%),
          radial-gradient(ellipse at 85% 15%, rgba(0, 202, 255, .20), transparent 32%),
          radial-gradient(ellipse at 75% 90%, rgba(255, 73, 173, .20), transparent 34%),
          linear-gradient(135deg, #080d22 0%, #111b3b 48%, #10102b 100%);
        color: #f7f8ff;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    [data-testid="stSidebar"] {
        background: rgba(11, 17, 43, .68);
        border-right: 1px solid rgba(255,255,255,.12);
        backdrop-filter: blur(24px);
    }
    [data-testid="stSidebar"] > div:first-child { background: transparent; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2.5rem; max-width: 1500px; }
    h1, h2, h3, p, label { color: #f7f8ff; }
    .brand {
        font-size: 2.25rem; font-weight: 800; letter-spacing: -1.4px;
        background: linear-gradient(90deg,#ff73d1,#a58bff,#61eaff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .subhead { color: #bdc9e8; margin-top: -4px; font-size: .98rem; }
    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,.105), rgba(255,255,255,.035));
        border: 1px solid var(--glass-border);
        border-radius: 22px; padding: 1.15rem 1.25rem;
        box-shadow: 0 18px 55px rgba(0,0,0,.20), inset 0 1px 0 rgba(255,255,255,.10);
        backdrop-filter: blur(22px);
    }
    .mini-label {
        text-transform: uppercase; font-size: .72rem; font-weight: 700;
        letter-spacing: 1.7px; color: #9fb1e8; margin-bottom: .45rem;
    }
    .status-pill {
        display: inline-block; border: 1px solid rgba(66,235,216,.35);
        color: #7ff7e8; background: rgba(39,219,194,.10);
        padding: 6px 12px; border-radius: 999px; font-size: .8rem;
    }
    .user-question {
        font-weight: 800; font-size: 1.16rem; line-height: 1.55;
        background: linear-gradient(90deg,#ff5dc8 0%,#ffb45f 25%,#f9f871 43%,#5fffc7 62%,#64d8ff 80%,#b38bff 100%);
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent; color: transparent;
        overflow-wrap: anywhere;
    }
    .message-meta { color: #9fb0d9; font-size: .78rem; margin-bottom: .35rem; }
    .assistant-text { color: #f0f4ff; line-height: 1.75; font-size: .96rem; }
    .source-chip {
        display: inline-block; margin: 4px 5px 0 0; padding: 6px 10px;
        border: 1px solid rgba(157,181,255,.25); border-radius: 10px;
        background: rgba(20,35,76,.62); color: #dce7ff; font-size: .78rem;
    }
    .powered {
        text-align: right; color: #b9c7e8; font-size: .78rem;
        padding-top: .75rem; letter-spacing: .2px;
    }
    div.stButton > button, div[data-testid="stFormSubmitButton"] button {
        border-radius: 12px; border: 1px solid rgba(148,161,255,.55);
        background: linear-gradient(110deg, rgba(117,83,255,.95), rgba(40,157,255,.9));
        color: white; font-weight: 700; min-height: 2.65rem;
        transition: transform .18s ease, box-shadow .18s ease;
    }
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-1px); box-shadow: 0 8px 24px rgba(83,112,255,.25);
        border-color: rgba(255,255,255,.75); color: white;
    }
    div[data-testid="stFileUploader"] section {
        border: 1px dashed rgba(154,169,255,.62);
        background: rgba(255,255,255,.045); border-radius: 16px;
    }
    div[data-testid="stTextInput"] input, div[data-testid="stChatInput"] textarea {
        background: rgba(255,255,255,.075); color: white;
        border: 1px solid rgba(255,255,255,.18); border-radius: 14px;
    }
    .stAlert { background: rgba(255,255,255,.07); border-radius: 14px; }
    hr { border-color: rgba(255,255,255,.12); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- Session state --------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex[:12]
if "processed_names" not in st.session_state:
    st.session_state.processed_names = set()
if "documents" not in st.session_state:
    st.session_state.documents = []
if "chat" not in st.session_state:
    st.session_state.chat = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "db_dir" not in st.session_state:
    st.session_state.db_dir = tempfile.mkdtemp(prefix="documind_")
if "embeddings" not in st.session_state:
    st.session_state.embeddings = None

# ----------------------------- Helpers --------------------------------
@st.cache_resource(show_spinner="Loading the embedding model…")
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={
            "token": os.getenv("HF_TOKEN")
        },
        encode_kwargs={
            "batch_size": 32,
            "normalize_embeddings": True
        }
    )

def get_llm():
    if not os.getenv("GROQ_API_KEY"):
        return None
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        temperature=0.2,
        api_key=os.getenv("GROQ_API_KEY"),
    )

def process_pdfs(uploaded_files):
    """Ingest new PDFs into this browser session's own Chroma collection."""
    new_files = [f for f in uploaded_files if f.name not in st.session_state.processed_names]
    if not new_files:
        return 0

    embeddings = load_embeddings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_chunks = []
    successful_names = []

    progress = st.progress(0, text="Preparing your documents…")
    for index, uploaded_file in enumerate(new_files):
        try:
            safe_name = Path(uploaded_file.name).name
            temp_path = Path(st.session_state.db_dir) / f"{uuid.uuid4().hex}_{safe_name}"
            temp_path.write_bytes(uploaded_file.getvalue())

            pages = PyPDFLoader(str(temp_path)).load()
            for page in pages:
                page.metadata["source"] = safe_name
            chunks = splitter.split_documents(pages)
            if chunks:
                all_chunks.extend(chunks)
                successful_names.append(safe_name)
            else:
                st.warning(f"`{safe_name}` did not contain extractable text.")
        except Exception as exc:
            st.error(f"Could not process **{uploaded_file.name}**: {exc}")
        progress.progress((index + 1) / len(new_files), text=f"Reading {uploaded_file.name}…")

    if all_chunks:
        collection_name = f"docs_{st.session_state.session_id}"
        if st.session_state.vector_store is None:
            st.session_state.vector_store = Chroma.from_documents(
                documents=all_chunks,
                embedding=embeddings,
                collection_name=collection_name,
                persist_directory=st.session_state.db_dir,
            )
        else:
            st.session_state.vector_store.add_documents(all_chunks)

        for name in successful_names:
            st.session_state.processed_names.add(name)
            st.session_state.documents.append(name)

    progress.empty()
    return len(successful_names)

def answer_question(question):
    llm = get_llm()
    if llm is None:
        st.error("Groq API key is missing. Add `GROQ_API_KEY` to your local `.env` or your hosting provider's Secrets.")
        return None, []

    if st.session_state.vector_store is None:
        return "Upload and process at least one PDF before asking a question.", []

    retriever = st.session_state.vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5},
    )
    docs = retriever.invoke(question)
    if not docs:
        return "I could not find the answer in the document.", []

    context = "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'PDF')}, page {doc.metadata.get('page', 0) + 1}]\n{doc.page_content}"
        for doc in docs
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are DocuMind, a helpful document question-answering assistant.
Answer using only the provided document context. If the answer is not present in the context, say:
"I could not find the answer in the document."
Be clear and concise. Do not invent sources."""),
        ("human", "Context:\n{context}\n\nQuestion:\n{question}"),
    ])
    response = llm.invoke(prompt.invoke({"context": context, "question": question}))
    sources = []
    seen = set()
    for doc in docs:
        source = doc.metadata.get("source", "PDF")
        page = doc.metadata.get("page", 0) + 1
        key = (source, page)
        if key not in seen:
            sources.append(key)
            seen.add(key)
    return response.content, sources

# ----------------------------- Sidebar ---------------------------------
with st.sidebar:
    if LOGO_PATH.is_file():
        st.image(str(LOGO_PATH), width=90)
    st.markdown(
        """
        <div style="padding:0 4px 20px 4px;">
          <div style="font-size:2.0rem;font-weight:800;background:linear-gradient(90deg,#ff72d2,#8c9dff,#59e7ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">DocuMind</div>
          <div style="color:#b9c7e8;font-size:.9rem;">Your PDFs. One conversation.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="mini-label">Your knowledge base</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Drop PDFs here or browse",
        type=["pdf"],
        accept_multiple_files=True,
        help="Select multiple PDFs at once. You can add more PDFs later.",
        label_visibility="collapsed",
    )
    st.caption("PDF files only · Select multiple files")
    if st.button("✦  Process selected PDFs", use_container_width=True, disabled=not uploaded_files):
        with st.spinner("Embedding your documents… this may take a moment on first use."):
            count = process_pdfs(uploaded_files)
        if count:
            st.success(f"Processed {count} new PDF(s).")
        elif uploaded_files:
            st.info("No new PDFs to process.")

    st.markdown("---")
    st.markdown('<div class="mini-label">Uploaded documents</div>', unsafe_allow_html=True)
    if st.session_state.documents:
        for filename in st.session_state.documents:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"📄 <span style='font-size:.83rem;overflow-wrap:anywhere'>{filename}</span>", unsafe_allow_html=True)
            with col2:
                if st.button("×", key=f"remove_{filename}", help="Remove this document from the list"):
                    st.session_state.documents.remove(filename)
                    st.session_state.processed_names.discard(filename)
                    # Chroma does not provide simple per-file removal without IDs here.
                    # Tell the user to rebuild the session collection to fully delete indexed chunks.
                    st.warning("Removed from the visible list. To fully remove its indexed chunks, clear the knowledge base and re-upload the PDFs.")
                    st.rerun()
    else:
        st.markdown("<div style='color:#9eadd2;font-size:.85rem'>No documents yet. Upload a PDF to begin.</div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🧹  Clear knowledge base", use_container_width=True):
        st.session_state.vector_store = None
        st.session_state.processed_names = set()
        st.session_state.documents = []
        st.session_state.chat = []
        st.session_state.db_dir = tempfile.mkdtemp(prefix="documind_")
        st.session_state.session_id = uuid.uuid4().hex[:12]
        st.rerun()

    st.markdown(
        """
        <div style="margin-top:22px;padding:13px;border:1px solid rgba(255,255,255,.12);
        border-radius:15px;background:rgba(255,255,255,.04);color:#aebee4;font-size:.78rem;line-height:1.6">
        <b style="color:#eef2ff">Privacy note</b><br>
        Documents are isolated to this app session. This demo uses temporary local storage; files may not persist after a restart.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------- Main UI ---------------------------------
left, right = st.columns([1.55, 1], vertical_alignment="center")
with left:
    st.markdown('<div class="brand">DocuMind - a RAG based pdf Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="subhead">A little less searching. A lot more understanding.</div>', unsafe_allow_html=True)
with right:
    st.markdown(
        '<div class="powered">POWERED BY &nbsp; ⚡ Groq &nbsp; · &nbsp; 🤗 Hugging Face &nbsp; · &nbsp; ◉ ChromaDB</div>',
        unsafe_allow_html=True,
    )

st.write("")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="glass-card"><div class="mini-label">Documents loaded</div><div style="font-size:1.35rem;font-weight:800">{len(st.session_state.documents)}</div><div style="color:#9eadd2;font-size:.8rem">PDFs in this session</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="glass-card"><div class="mini-label">Assistant</div><div style="font-size:1.35rem;font-weight:800">Ready when you are</div><div style="color:#9eadd2;font-size:.8rem">Answers grounded in your PDFs</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="glass-card"><div class="mini-label">Retrieval mode</div><div style="font-size:1.35rem;font-weight:800">MMR Search</div><div style="color:#9eadd2;font-size:.8rem">Relevant and diverse chunks</div></div>', unsafe_allow_html=True)

st.write("")
# st.markdown('<div class="glass-card">', unsafe_allow_html=True)
head1, head2 = st.columns([5, 1])
with head1:
    st.markdown("### ◇ Chat with your documents")
    st.markdown(
        f'<span class="status-pill">● {"Knowledge base ready" if st.session_state.vector_store is not None else "Waiting for PDFs"}</span>',
        unsafe_allow_html=True,
    )
with head2:
    if st.button("Clear chat", use_container_width=True):
        st.session_state.chat = []
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if not st.session_state.chat:
    st.markdown(
        """
        <div style="text-align:center;padding:0px 15px 25px">
          <div style="font-size:3.1rem;margin-bottom:8px">✧</div>
          <div style="font-size:1.35rem;font-weight:750">Ask your documents anything.</div>
          <div style="color:#b9c7e8;margin-top:8px">Upload PDFs in the sidebar, process them, then start a conversation.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    example_cols = st.columns(6)
    examples = ["Summarize the key concepts", "Explain this topic simply", "What are the main takeaways?", "Explain in detail","Explain in simple terms","Explain like I'm 5"]
    for i, example in enumerate(examples):
        with example_cols[i]:
            if st.button(example, key=f"example_{i}", use_container_width=True):
                st.session_state.pending_question = example
                st.rerun()

for idx, message in enumerate(st.session_state.chat):
    if message["role"] == "user":
        st.markdown(
            f'<div style="margin:14px 0 6px 0"><div class="message-meta">YOU &nbsp; · &nbsp; QUESTION</div><div class="user-question">{message["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="message-meta">✦ DOCUMIND</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="assistant-text">{message["content"]}</div>', unsafe_allow_html=True)
        if message.get("sources"):
            st.markdown('<div class="message-meta" style="margin-top:12px">▤ SOURCES</div>', unsafe_allow_html=True)
            chips = "".join(
                f'<span class="source-chip">📄 {name} · p. {page}</span>'
                for name, page in message["sources"]
            )
            st.markdown(chips, unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# A form avoids submitting the same prompt repeatedly on unrelated reruns.
pending = st.session_state.pop("pending_question", "")
with st.form("question_form", clear_on_submit=True):
    qcol, bcol = st.columns([6, 1])
    with qcol:
        question = st.text_input(
            "Ask a question",
            value=pending,
            placeholder="Ask a question about your PDFs…",
            label_visibility="collapsed",
        )
    with bcol:
        submitted = st.form_submit_button("➤  Ask", use_container_width=True)

if submitted and question.strip():
    user_question = question.strip()
    st.session_state.chat.append({"role": "user", "content": user_question})
    with st.spinner("Searching your documents and thinking…"):
        answer, sources = answer_question(user_question)
    if answer is not None:
        st.session_state.chat.append({"role": "assistant", "content": answer, "sources": sources})
    st.rerun()

st.markdown(
    '<div style="text-align:center;color:#8798c3;font-size:.76rem;padding:22px 0 0">DocuMind · Built with Streamlit, LangChain, ChromaDB & Groq</div>',
    unsafe_allow_html=True,
)