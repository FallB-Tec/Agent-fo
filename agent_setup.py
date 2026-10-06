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
]

#Tools
#1.Simple tool to get the current time
@tool("get_date",description="Get the current date in the format YYYY-MM-DD and the day of the week",return_direct=False)
def get_date() -> str:
    return datetime.now().strftime("%Y-%m-%d %A")

#2.Tool to retrieve relevant financial documents from the vectorstore
@tool("retrieve_documents",description=
    "Retrieve relevant information from the company's financial filings "
    "stored in the vector database. Use this tool when answering questions "
    "about information contained in 10-K filings, including business "
    "operations, financial performance, revenue, expenses, risks, assets, "
    "liabilities, cash flow, business segments, management discussion, "
    "accounting information, and other filing-specific information. "
    "When the user specifies a company, include the company name in the "
    "query so the retrieval system can identify the relevant documents. "
    "Use this tool for document-based financial information, not for "
    "current or historical stock prices, trading volume, or stock-price "
    "calculations. For those requests, use the appropriate stock-data or "
    "metrics tool. Base document-related answers only on information "
    "supported by the retrieved documents.",return_direct=False)
def retrieve_documents(query: str) -> list:
    relevant_docs = retriever.invoke(query)
    
    # print("Collection count:", db._collection.count())

    # print("--Context--")

    # for doc in relevant_docs:
        # print(f"Retrieved document: {doc.page_content[:500]}...")  # Print the first 500 characters of the document content

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

        After determining the correct dates, see if it is a week end day than adjust the day then call get_company_stock_info  with
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
@tool("company_metrics", description=(
        "Calculate a specific stock metric for a ticker over an inclusive "
        "date range. Use for: highest_close, lowest_close, average_close, "
        "highest_high, lowest_low, average_high, average_low, "
        "average_volume, price_change, and percentage_change. "
        "Use highest_close/lowest_close for closing prices and "
        "highest_high/lowest_low for intraday High/Low prices. "
        "All numerical calculations are performed from historical market "
        "data, not by the language model."
    ))
def company_metrics(
    ticker: str,
    start_date: Date,
    end_date: Date,
    metric: Metric,
) -> dict:
    """
    Calculate stock metrics for a company over a specified period.
    """

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    if start_date > end_date:
        return {
            "success": False,
            "error": "start_date cannot be after end_date."
        }

    try:
        analyzer = StockAnalyzer(ticker)

        # --------------------------------------------------
        # FETCH STOCK DATA
        # --------------------------------------------------

        stock_data = analyzer.get_stock_data(
            start_date=start_date,
            end_date=end_date,
        )

        if not stock_data:
            return {
                "success": False,
                "error": f"No stock data found for {ticker}."
            }

        first_day = stock_data[0]
        last_day = stock_data[-1]

        # --------------------------------------------------
        # HIGHEST / LOWEST
        # --------------------------------------------------

        if metric == "highest_close":
            day = max(stock_data, key=lambda x: x.close)

            result = {
                "value": day.close,
                "date": day.date.isoformat(),
            }

        elif metric == "lowest_close":
            day = min(stock_data, key=lambda x: x.close)

            result = {
                "value": day.close,
                "date": day.date.isoformat(),
            }

        elif metric == "highest_high":
            day = max(stock_data, key=lambda x: x.high)

            result = {
                "value": day.high,
                "date": day.date.isoformat(),
            }

        elif metric == "lowest_low":
            day = min(stock_data, key=lambda x: x.low)

            result = {
                "value": day.low,
                "date": day.date.isoformat(),
            }

        # --------------------------------------------------
        # AVERAGES
        # --------------------------------------------------

        elif metric == "average_close":
            value = sum(day.close for day in stock_data) / len(stock_data)

            result = {
                "value": value,
                "trading_days": len(stock_data),
            }

        elif metric == "average_high":
            value = sum(day.high for day in stock_data) / len(stock_data)

            result = {
                "value": value,
                "trading_days": len(stock_data),
            }

        elif metric == "average_low":
            value = sum(day.low for day in stock_data) / len(stock_data)

            result = {
                "value": value,
                "trading_days": len(stock_data),
            }

        elif metric == "average_volume":
            value = sum(day.volume for day in stock_data) / len(stock_data)

            result = {
                "value": value,
                "trading_days": len(stock_data),
            }

        # --------------------------------------------------
        # PRICE CHANGES
        # --------------------------------------------------

        elif metric == "price_change":
            value = last_day.close - first_day.close

            result = {
                "value": value,
                "start": {
                    "date": first_day.date.isoformat(),
                    "close": first_day.close,
                },
                "end": {
                    "date": last_day.date.isoformat(),
                    "close": last_day.close,
                },
            }

        elif metric == "percentage_change":
            value = (
                (last_day.close - first_day.close)
                / first_day.close
            ) * 100

            result = {
                "value": value,
                "start": {
                    "date": first_day.date.isoformat(),
                    "close": first_day.close,
                },
                "end": {
                    "date": last_day.date.isoformat(),
                    "close": last_day.close,
                },
            }

        # --------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------

        return {
            "success": True,
            "ticker": ticker.upper(),
            "metric": metric,
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
            "data": result,
        }

    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
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
class ResponseFormat(BaseModel):
    summary: str
    data: dict = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)