from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import create_retriever_tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import ingestion_pip

#Model, it is a local model
model = ChatOllama(
     base_url="http://localhost:11434",
    model="qwen3",
    temperature=0.1
)



def main():
    return 0;
