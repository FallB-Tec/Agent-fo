from pyexpat import model

from langchain.agents import create_agent
from langchain.tools import tool,ToolRuntime
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, data
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator
import yfinance as yf
import datetime 


#class
class StockData(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the company.")
    open: float = Field(..., description="The opening price of the stock")
    high: float = Field(..., description="The highest price of the stock")
    low: float = Field(..., description="The lowest price of the stock")
    close: float = Field(..., description="The closing price of the stock")
    volume: int = Field(..., description="The volume of stocks traded")
    
    #validate stock data model
    @model_validator(mode="after")
    def validate_stock_data(cls, model):
        if model.open <= 0:
            raise ValueError("Opening price must be greater than zero.")
        if model.open < 0 or model.high < 0 or model.low < 0 or model.close < 0 or model.volume < 0:
            raise ValueError("Stock prices and volume must be non-negative.")
        if model.ticker == "":
            raise ValueError("Ticker symbol cannot be empty.")
        return model 
    
    #computed field
    @computed_field
    @property
    def price_change(self) -> float:
        return self.close - self.open
    
    @computed_field
    @property
    def price_change_percent(self) -> float:
            return (self.price_change / self.open) * 100
    
    @computed_field
    @property
    def daily_range(self) -> float:
        return self.high - self.low

class StockDataInput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol, such as AAPL.")
    start_date: datetime.date = Field(..., description="Start date in YYYY-MM-DD format.")
    end_date: datetime.date = Field(..., description="End date in YYYY-MM-DD format.")
    
    @field_validator("ticker")
    def validate_ticker(cls, value):
        if not value.isalnum():
            raise ValueError("Ticker symbol must be alphanumeric.")
        return value.upper()
    
    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value):
        return value.upper()

    @field_validator("start_date", "end_date")
    def validate_date_format(cls, value):
        if not isinstance(value, datetime.date):
            raise ValueError("Date must be in YYYY-MM-DD format.")
        return value
    
    @model_validator(mode="after")
    def validate_dates(cls, model):
        if model.start_date > model.end_date:
            raise ValueError("Start date must be before end date.")
        return model

 
 
 #OOP for stock Analysis class StockAnalyzer:
def __init__(self, ticker: str):
    self.ticker = yf.Ticker(ticker)

    def get_stock_data(self, start_date: str, end_date: str) -> StockData:
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
 