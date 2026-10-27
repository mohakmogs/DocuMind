

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


embeddings = HuggingFaceEmbeddings()

vector_store = Chroma(
    persist_directory="project_db",
    embedding_function=embeddings
)

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k":10,
        "lambda_mult": 0.5
        }
)








# Initialize Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    
    temperature=0.7
)

prompt=ChatPromptTemplate.from_messages([
    ("system","""You are a helpful AI agent. 
    Use only the provided context to answer the question. 

    If the answer is not present in the context, say:"I could not find the answer in the document." 
"""),
    ("human","""
Context:
{context}
Question:
{question}
""")
])


print("Welcome to the RAG system. Type '0' to quit.")

while True:
    query=input("You : ")
    if query=="0":
        print("Exiting the RAG system. Goodbye!")
        break

    docs=retriever.invoke(query)

    context="\n\n".join([doc.page_content for doc in docs])

    final_prompt=prompt.invoke({"context": context, "question": query})

    response=llm.invoke(final_prompt)

    print("\n  AI : ",response.content,"\n")





