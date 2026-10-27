from langchain_community.document_loaders import TextLoader

data = TextLoader(r"resume.pdf")

doc=data.load()

print(doc)

