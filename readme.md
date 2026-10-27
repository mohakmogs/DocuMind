::: {align="center"}
# 🧠 DocuMind

### Your PDFs. One conversation.

**An AI-powered PDF question-answering assistant built with
Retrieval-Augmented Generation (RAG).**

`<br/>`{=html}

```{=html}
<h2>
```
`<a href="PASTE_YOUR_LIVE_APP_URL_HERE">`{=html}🚀 OPEN DOCUMIND ---
LIVE APP`</a>`{=html}
```{=html}
</h2>
```
*Replace `PASTE_YOUR_LIVE_APP_URL_HERE` with your deployed Streamlit app
URL.*

`<br/>`{=html}

`<img src="img/documind.png" alt="DocuMind logo" width="150"/>`{=html}
:::

------------------------------------------------------------------------

## 📸 App Preview

> Add two screenshots of your deployed app to the `screenshots/` folder
> using the filenames below. These images will appear here once you push
> them to GitHub.

```{=html}
<table>
```
```{=html}
<tr>
```
```{=html}
<td align="center" width="50%">
```
`<strong>`{=html}1. DocuMind
Interface`</strong>`{=html}`<br/>`{=html}`<br/>`{=html}
`<img src="screenshots/documind-home.png" alt="DocuMind home screen" width="100%"/>`{=html}
```{=html}
</td>
```
```{=html}
<td align="center" width="50%">
```
`<strong>`{=html}2. Chat with Your
Documents`</strong>`{=html}`<br/>`{=html}`<br/>`{=html}
`<img src="screenshots/documind-chat.png" alt="DocuMind PDF chat screen" width="100%"/>`{=html}
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
</table>
```

------------------------------------------------------------------------

## ✨ About DocuMind

**DocuMind** lets you upload PDF documents and ask questions about their
contents in natural language. It retrieves relevant passages from your
documents and uses a language model to generate answers grounded in the
retrieved context.

Instead of manually searching through long PDFs, you can ask questions,
explore key concepts, and review source references from the documents
you uploaded.

## 🚀 Features

-   **PDF question answering** --- ask natural-language questions about
    uploaded PDFs.
-   **Retrieval-Augmented Generation (RAG)** --- retrieves relevant
    document chunks before generating an answer.
-   **Semantic embeddings** --- converts text chunks into vectors for
    similarity-based retrieval.
-   **ChromaDB vector store** --- stores and searches document
    embeddings.
-   **MMR retrieval** --- helps retrieve relevant and diverse context
    chunks.
-   **Source references** --- displays source filenames and page numbers
    for retrieved content.
-   **Multiple PDF uploads** --- add more than one PDF to a session.
-   **Chat interface** --- ask follow-up questions in a Streamlit
    interface.
-   **Responsive visual design** --- dark gradient styling and
    glass-inspired UI.
-   **Hosted LLM** --- uses the Groq API to generate responses.
-   **Hugging Face embeddings** --- uses
    `sentence-transformers/all-MiniLM-L6-v2` for local embedding
    generation.

## 🧰 Tech Stack

  Technology                           Purpose
  ------------------------------------ ----------------------------------------
  Python                               Application logic
  Streamlit                            Web interface and deployment
  LangChain                            Document processing and RAG components
  Groq API                             Language-model responses
  Hugging Face Sentence Transformers   Text embeddings
  `all-MiniLM-L6-v2`                   Embedding model
  ChromaDB                             Vector storage and retrieval
  PyPDF / PyPDFLoader                  PDF text extraction
  RecursiveCharacterTextSplitter       Splitting documents into chunks

## 🔄 How It Works

1.  **Upload** --- select one or more PDF files.
2.  **Extract** --- DocuMind extracts text from the PDFs.
3.  **Split** --- text is divided into overlapping chunks.
4.  **Embed** --- the embedding model converts chunks into vectors.
5.  **Store** --- vectors and document chunks are added to ChromaDB.
6.  **Retrieve** --- the user's question is used to retrieve relevant
    chunks using MMR search.
7.  **Generate** --- the retrieved context and question are sent to the
    Groq-hosted language model.
8.  **Display** --- the answer and available source filename/page
    references are shown in the chat.

``` text
PDF Upload
    │
    ▼
Text Extraction
    │
    ▼
Chunking
    │
    ▼
Hugging Face Embeddings
    │
    ▼
ChromaDB Vector Store
    │
User Question ──► Retriever (MMR)
                       │
                       ▼
              Relevant PDF Context
                       │
                       ▼
                  Groq LLM
                       │
                       ▼
             Answer + Source References
```

## 🖥️ Run Locally

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR_GITHUB_USERNAME/DocuMind.git
cd DocuMind
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub username. If your
repository URL differs, use the URL shown on GitHub.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python
directly or follow the Python documentation for your execution-policy
settings.

### 3. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

``` env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
HF_TOKEN=your_huggingface_read_token
```

-   Get a Groq API key from the [Groq
    Console](https://console.groq.com/keys).
-   A Hugging Face token can be created in [Hugging Face
    settings](https://huggingface.co/settings/tokens). For this public
    embedding model, a token is generally optional, but authentication
    may help with Hub rate limits.
-   Use a Groq model name that is currently available to your account.

**Never commit `.env` or publish API keys.** Keep `.env` in
`.gitignore`. For Streamlit Community Cloud, configure the same values
in the app's **Settings → Secrets** instead of uploading `.env`.

### 5. Start the app

``` bash
streamlit run app.py
```

Streamlit will print a local URL in the terminal, usually
`http://localhost:8501`.

## ☁️ Deployment

DocuMind can be deployed using [Streamlit Community
Cloud](https://share.streamlit.io/).

1.  Push the project to GitHub.
2.  Sign in to Streamlit Community Cloud with GitHub.
3.  Create an app and select this repository.
4.  Select the `main` branch and set the main file path to `app.py`.
5.  Add your secrets in the Streamlit app's **Secrets** settings:

``` toml
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "openai/gpt-oss-120b"
HF_TOKEN = "your_huggingface_read_token"
```

6.  Deploy and review the app logs if startup fails.

The first start can take longer because dependencies and the embedding
model may need to be downloaded.

## 🔐 Security & Privacy Notes

-   Do not commit `.env`, API keys, access tokens, or other credentials.
-   Configure production credentials through Streamlit Secrets.
-   Treat uploaded documents as potentially sensitive; only upload
    documents you are authorized to process.
-   This app uses a hosted LLM API, so retrieved document context may be
    sent to the configured provider to generate answers.
-   The current demo uses temporary/session storage for its vector
    database. Uploaded files and indexed vectors may not persist after
    restarts.
-   Do not use the app to process confidential documents unless you have
    reviewed the hosting, storage, and API-provider privacy
    requirements.

## ⚠️ Current Limitations

-   PDF text extraction works best with text-based PDFs. Scanned PDFs
    may require OCR before their contents can be searched.
-   Answer quality depends on PDF text quality, chunking, retrieval, and
    the configured language model.
-   The first embedding-model download and initial document indexing may
    take time.
-   Temporary Chroma storage means indexed documents may need to be
    uploaded and processed again after a restart.
-   The application is a project/demo and may need additional access
    controls, persistent storage, usage limits, and monitoring for
    production use.

## 🗂️ Project Structure

``` text
DocuMind/
├── app.py
├── main.py
├── create_db.py
├── requirements.txt
├── .gitignore
├── img/
│   └── documind.png
├── document loaders/
├── text spitting/
└── vector store/
```

The exact contents may vary as the project evolves.

## 🛠️ Troubleshooting

**`ModuleNotFoundError` during deployment** - Confirm the missing
package is listed in `requirements.txt`. - Commit and push the updated
requirements file. - Check the Streamlit deployment logs for the package
installation result.

**Groq API key missing** - Check that `GROQ_API_KEY` is set in Streamlit
Secrets. - Confirm the code reads the secret or environment variable
correctly. - Never paste the key into public logs or GitHub issues.

**Hugging Face download is slow** - The first run downloads the
embedding model. Later runs can reuse it if the model cache persists. -
Public model access generally does not require a token, but
authentication can help with rate limits.

**Answers are inaccurate or say the answer was not found** - Try a
text-based PDF with selectable text. - Ask a more specific question
using terms from the document. - Check whether the expected content is
present in the uploaded PDF.

## 🛣️ Possible Future Improvements

-   Persistent vector storage across sessions and restarts.
-   Better document removal and per-user knowledge-base isolation.
-   OCR support for scanned PDFs.
-   Improved upload validation and file-size limits.
-   Streaming answers and clearer indexing progress.
-   Automated tests and more robust error handling.
-   Additional embedding and LLM provider options.

## 👨‍💻 Author

**Mohak Pandey**

-   GitHub: [@mohakmogs](https://github.com/mohakmogs)

## 📄 License

No license is specified yet. Add a `LICENSE` file if you want to grant
others explicit permission to reuse, modify, or distribute this project.

------------------------------------------------------------------------

::: {align="center"}
**DocuMind --- less searching, more understanding.** 🧠📄
:::
