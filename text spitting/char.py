from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="",#default is "\n\n"
    chunk_size=10,
    chunk_overlap=1
)

data=TextLoader(r"C:\Users\mohak\OneDrive\Desktop\gen ai 2 rag\text spitting\text.txt")

docs=data.load()

chunks=splitter.split_documents(docs)

for i in chunks:
    print(i.page_content)
    print("--------------------------------------------------")
    print("--------------------------------------------------")

print(len(chunks))
