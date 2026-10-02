from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import create_retriever_tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import ingestion_pip
import agent_setup

#Model, it is a local model
model = ChatOllama(
     base_url="http://localhost:11434",
    model="qwen3",
    temperature=0.1
)


#Orchestrator function
def main():
   #for now we will just call the vector_db_create_update function to create or update the vector database to populate the vectorstore with the documents and their embeddings
    # vector_db_create_update()
    
    #basic retrieval to test the similarity search and retrieval of relevant documents from the vectorstore
    agent_setup.retrieve_documents("What is the revenue of Amazon in 2022?")

if __name__ == "__main__":
    main()


#separate function to create or update the vector database 
def vector_db_create_update():
     #Load the documents
    documents = ingestion_pip.load_document(docs_path="C:\\Users\\PcSuu\\OneDrive\\Desktop\\Companies_10k_filing")
        
    # print(f"Documents loaded: {len(documents)}")
        
     #Split the documents into chunks
    chunks = ingestion_pip.split_documents(documents)
        
    # print(f"Chunks created: {len(chunks)}")
    print(f"First chunk: {chunks[0].page_content}")
        
    vectorstore = ingestion_pip.create_vectorstore(chunks)
    print(f"Vectorstore created with {vectorstore._collection.count()} vectors")
    
    