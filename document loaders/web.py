
import os

os.environ["USER_AGENT"] = "Mozilla/5.0 (compatible; MyRAGBot/1.0)"

from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup

data = WebBaseLoader("https://www.amazon.in").load()

print(data)

