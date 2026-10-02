from langchain.agents import create_agent
from langchain.tools import tool,ToolRuntime
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field
from datetime import datetime



#Class




#Tools
#1.Simple tool to get the current time
@tool("get_date",description="Get the current date in the format YYYY-MM-DD",return_direct=True)
def get_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

#1.Tool to retrieve relevant financial documents from the vectorstore
# @tool("retrieve_documents",description="Retrieve relevant documents from the vectorstore based on a query",return_direct=True)
def retrieve_documents(query: str) -> list:
    relevant_docs = retriever.invoke(query)
    
    print("Collection count:", db._collection.count())

    print("--Context--")

    for doc in relevant_docs:
        print(f"Retrieved document: {doc.page_content[:500]}...")  # Print the first 500 characters of the document content

    return relevant_docs

#agent 

#function
embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="db/chroma_db",
    embedding_function=embedding_function,
    collection_metadata={"hnsw:space": "cosine"}
)

retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 3,
        "score_threshold": 0.3
    }
)