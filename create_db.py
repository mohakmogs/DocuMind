#load pdf
#create chunks using text splitter
#create embeddings using hugging face
#create vector store using chroma or storing in db

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

data = PyPDFLoader(r"C:\Users\mohak\OneDrive\Desktop\gen ai 2 rag\document loaders\deep-learning-material-dept-ece-ase-blr-1.pdf")
doc=data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200)

chunks=splitter.split_documents(doc)
# print(len(chunks))

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-mpnet-base-v2",
#     model_kwargs={
#         "token": os.getenv("HUGGINGFACEHUB_API_KEY")
#     }
# )


vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="project_db"
)



