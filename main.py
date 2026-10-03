from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from agent import  run_agent
import ingestion_pip


#Orchestrator function
def main():
   #for now we will just call the vector_db_create_update function to create or update the vector database to populate the vectorstore with the documents and their embeddings
    # vector_db_create_update()
    
    #basic retrieval to test the similarity search and retrieval of relevant documents from the vectorstore
    # agent_setup.retrieve_documents("What is the revenue of Amazon in 2022?")
    
    run_agent()


if __name__ == "__main__":
    main()

    
    
    