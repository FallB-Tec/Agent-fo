from os import error

from langchain.agents import create_agent
from langchain.tools import tool,ToolRuntime
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field
from datetime import datetime
import yfinance as yf
from stock_tool_logic import StockAnalyzer, StockDataInput

#Tools
#1.Simple tool to get the current time
@tool("get_date",description="Get the current date in the format YYYY-MM-DD",return_direct=False)
def get_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

#2.Tool to retrieve relevant financial documents from the vectorstore
@tool("retrieve_documents",description="Retrieve relevant documents from the vectorstore based on a query",return_direct=False)
def retrieve_documents(query: str) -> list:
    relevant_docs = retriever.invoke(query)
    
    print("Collection count:", db._collection.count())

    print("--Context--")

    for doc in relevant_docs:
        print(f"Retrieved document: {doc.page_content[:500]}...")  # Print the first 500 characters of the document content

    return relevant_docs

#3.Tool to get stock information 
@tool(
    "get_company_stock_info",
    description=(
        """Retrieve historical stock market data for a company. 
        Use this tool when stock price or trading-volume information is needed. 
        Provide the company's ticker symbol and the start and end dates 
        for the requested historical period.You are a financial assistant.
        
        When a user's request depends on the current date or time, especially
        relative expressions such as "today", "yesterday", "3 days ago",
        "last week", or "this month", you MUST call get_time first.

        Use the result of get_time as the reference point for calculating dates.
        Do not assume, guess, or use your internal knowledge for the current
        date or time.

        After determining the correct dates, call get_company_stock_info with
        the calculated dates.
        
        Use the date returned by get_time as the reference point for calculating
        the requested date range. Do not assume or invent the current date."""
    ),
    return_direct=False,
)
def get_company_stock_info(
    ticker: str,
    start_date: str,
    end_date: str,
) -> list:
    
    #catching any ValueError exceptions that may arise from invalid input data
    try:
        input_data = StockDataInput(ticker=ticker, start_date=start_date, end_date=end_date)
        stock_analyzer = StockAnalyzer(input_data.ticker)
        stock_data = stock_analyzer.get_stock_data(input_data.start_date, input_data.end_date)

        return stock_data
    except ValueError as e:
        return {
            "error": str(e)
        }
   
       

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