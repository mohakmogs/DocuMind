from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter


splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)

data = PyPDFLoader(r"C:\Users\mohak\OneDrive\Desktop\gen ai 2 rag\document loaders\resume.pdf")

doc=data.load()

chunks=splitter.split_documents(doc)

print(len(chunks))

