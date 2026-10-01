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
    #Load the documents
    documents = ingestion_pip.load_document(docs_path="Companies_10k_filing")
    
    print(f"Documents loaded: {len(documents)}")
    
    #Split the documents into chunks
    chunks = ingestion_pip.split_documents(documents)
    
    print(f"Chunks created: {len(chunks)}")
    print(f"First chunk: {chunks[0].page_content}")
    


if __name__ == "__main__":
    main()
