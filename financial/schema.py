"""
Financial Data Model

This module defines the `FinancialData` model class using the Pydantic library.
The model represents a financial data record with properties for symbol, date, open price, close price, and volume.
"""

from datetime import date

from pydantic import BaseModel


class FinancialData(BaseModel):
    """
    Financial Data Model

    This class represents a financial data record with properties for symbol, date, open price, close price, and volume.
    """
    symbol: str
    date: date
    open_price: float
    close_price: float
    volume: int

    class Config:
        orm_mode = True
