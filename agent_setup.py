from dataclasses import dataclass
from typing import Literal
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field
from datetime import date as Date, datetime
from stock_tool_logic import StockAnalyzer, StockDataInput


#constant
Metric = Literal[
    "highest_close",
    "lowest_close",
    "average_close",
    "price_change",
    "percentage_change",
    "highest_high",
    "lowest_low",
    "average_high",
    "average_low",
    "average_volume",
    "highest_close_date",
    "lowest_close_date",
]

#Tools
#1.Simple tool to get the current time
@tool("get_date",description="Get the current date in the format YYYY-MM-DD and the day of the week",return_direct=False)
def get_date() -> str:
    return datetime.now().strftime("%Y-%m-%d %A")

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

        After determining the correct dates, see if it is a week end day than adjust the day then call get_company_stock_info or company_metrics with
        the calculated dates.
        
        Use the date returned by get_time as the reference point for calculating
        the requested date range. Do not assume or invent the current date."""
    ),
    return_direct=False,
)
def get_company_stock_info(
    ticker: str,
    start_date: str,
    end_date: str
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
        
#tool to calculate metrics for stock data
@tool
def company_metrics(
    ticker: str,
    start_date: Date,
    end_date: Date,
    metric: Metric,
) -> dict:
    """
    Calculate metrics from historical stock data.

    Use this tool for questions about:
    - highest or lowest prices
    - highest or lowest closing prices
    - average prices
    - price changes
    - percentage changes
    - trading volume
    - dates of highest or lowest closing prices

    ticker:
        Stock ticker symbol, such as NVDA, AMZN, or AAPL.

    start_date:
        Beginning of the requested period.

    end_date:
        End of the requested period.

    metric:
        The metric to calculate.
    """

    try:
        analyzer = StockAnalyzer(ticker)

        # Retrieve raw stock data
        stock_data = analyzer.get_stock_data(
            start_date=start_date,
            end_date=end_date
        )

        if not stock_data:
            return {
                "success": False,
                "error": "No stock data found for the requested period."
            }

        # --------------------------------------------------
        # HIGH / LOW
        # --------------------------------------------------

        if metric == "highest_close":
            result = max(stock_data, key=lambda x: x.close)

            data = {
                "date": result.date.isoformat(),
                "close": result.close,
            }

        elif metric == "lowest_close":
            result = min(stock_data, key=lambda x: x.close)

            data = {
                "date": result.date.isoformat(),
                "close": result.close,
            }

        elif metric == "highest_high":
            result = max(stock_data, key=lambda x: x.high)

            data = {
                "date": result.date.isoformat(),
                "high": result.high,
            }

        elif metric == "lowest_low":
            result = min(stock_data, key=lambda x: x.low)

            data = {
                "date": result.date.isoformat(),
                "low": result.low,
            }

        # --------------------------------------------------
        # AVERAGES
        # --------------------------------------------------

        elif metric == "average_close":
            average = sum(
                day.close for day in stock_data
            ) / len(stock_data)

            data = {
                "average_close": average
            }

        elif metric == "average_high":
            average = sum(
                day.high for day in stock_data
            ) / len(stock_data)

            data = {
                "average_high": average
            }

        elif metric == "average_low":
            average = sum(
                day.low for day in stock_data
            ) / len(stock_data)

            data = {
                "average_low": average
            }

        elif metric == "average_volume":
            average = sum(
                day.volume for day in stock_data
            ) / len(stock_data)

            data = {
                "average_volume": average
            }

        # --------------------------------------------------
        # PRICE CHANGE
        # --------------------------------------------------

        elif metric == "price_change":
            first_close = stock_data[0].close
            last_close = stock_data[-1].close

            data = {
                "start_date": stock_data[0].date.isoformat(),
                "end_date": stock_data[-1].date.isoformat(),
                "start_close": first_close,
                "end_close": last_close,
                "price_change": last_close - first_close,
            }

        # --------------------------------------------------
        # PERCENTAGE CHANGE
        # --------------------------------------------------

        elif metric == "percentage_change":
            first_close = stock_data[0].close
            last_close = stock_data[-1].close

            percentage_change = (
                (last_close - first_close)
                / first_close
            ) * 100

            data = {
                "start_date": stock_data[0].date.isoformat(),
                "end_date": stock_data[-1].date.isoformat(),
                "start_close": first_close,
                "end_close": last_close,
                "percentage_change": percentage_change,
            }

        # --------------------------------------------------
        # DATES
        # --------------------------------------------------

        elif metric == "highest_close_date":
            result = max(stock_data, key=lambda x: x.close)

            data = {
                "date": result.date.isoformat(),
                "close": result.close,
            }

        elif metric == "lowest_close_date":
            result = min(stock_data, key=lambda x: x.close)

            data = {
                "date": result.date.isoformat(),
                "close": result.close,
            }

        else:
            return {
                "success": False,
                "error": f"Unsupported metric: {metric}"
            }

        return {
            "success": True,
            "ticker": ticker.upper(),
            "metric": metric,
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
            },
            "data": data,
        }

    except ValueError as e:
        return {
            "success": False,
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

#response format for agent
@dataclass
class ResponseFormat:
    summary: str
    data: dict
    metadata: dict