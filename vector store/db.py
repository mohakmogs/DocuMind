from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()



from langchain_core.documents import Document

docs=[
Document(page_content="Pandas are used in data science.", metadata={"source": "test1.txt"}),
Document(page_content="ANN is a type of deep learning model.", metadata={"source": "test2.txt"}),
Document(page_content="CNN stands for Convolutional Neural Network.", metadata={"source": "test3.txt"})
]
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="chroma_db"
)

result = vector_store.similarity_search("What is CNN?", k=2)

for i in result:
    print(i.page_content)
    print(i.metadata)
    