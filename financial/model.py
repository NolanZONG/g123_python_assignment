"""
Financial Data Model

This module defines an SQLAlchemy model for storing financial data in the MySQL database.
"""

from sqlalchemy import Column, Date, Integer, String, DECIMAL

from .database import Base


class FinancialData(Base):
    """
    represents a table named "financial_data"
    """
    __tablename__ = "financial_data"

    symbol = Column(String(16), primary_key=True)
    date = Column(Date, primary_key=True)
    open_price = Column(DECIMAL(20, 8))
    close_price = Column(DECIMAL(20, 8))
    volume = Column(Integer)
