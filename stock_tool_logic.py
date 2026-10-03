from langchain.agents import create_agent
from langchain.tools import tool,ToolRuntime
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, data
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field
import yfinance as yf


#class
class StockData(BaseModel):
    ticker: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    
#OOP for stock Analysis
class StockAnalyzer:
    def __init__(self, ticker: str):
        self.ticker = yf.Ticker(ticker)

    def get_stock_data(self,start_date: str,end_date: str) -> StockData:
        data = self.ticker.history(
            start=start_date,
            end=end_date)

        return StockData(
            ticker=self.ticker.ticker,
            open=float(data["Open"]),
            high=float(data["High"]),
            low=float(data["Low"]),
            close=float(data["Close"]),
            volume=int(data["Volume"]),
        )