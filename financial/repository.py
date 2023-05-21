"""
Financial Data Repository

This module provides a repository class for managing financial data in the database.
The `FinancialDataRepository` class interacts with the `FinancialData` model to perform operations.
"""

from typing import List, Tuple
from datetime import date

from .model import FinancialData
from .database import SessionLocal


class FinancialDataRepository:
    """
    This class provides methods for interacting with the financial data in the database.
    """
    def __init__(self):
        """
        Initializes the repository by creating an SQLAlchemy session.
        """
        self.session = SessionLocal()

    def upsert_financial_data(self, stock_quotes: List[Tuple[str, date, float, float, int]]) -> None:
        """
        Upserts financial data into the database based on the provided stock quotes.

        :param stock_quotes: A list of stock quotes to upsert into the database.
        :return: None
        """
        try:
            for symbol, date, open_price, close_price, volume in stock_quotes:
                self.session.merge(
                    FinancialData(
                        symbol=symbol,
                        date=date,
                        open_price=open_price,
                        close_price=close_price,
                        volume=volume,
                    )
                )
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_financial_data_by_date_range(
        self,
        symbol: str,
        start_date: date,
        end_date: date,
        limit: int = None,
        page: int = None
    ) -> Tuple[int, List[FinancialData]]:
        """
        Retrieves financial data from the database based on the provided parameters.

        :param symbol: The symbol of the financial data to query.
        :param start_date: The start date of the date range to filter records.
        :param end_date: The end date of the date range to filter records.
        :param limit: The maximum number of records to return per page.
        :param page: The page number of the records to retrieve.
        :return: A tuple containing the total count of financial data records matching the query
             and a list of FinancialData objects representing the retrieved financial data.
        """
        query_obj = self.session.query(FinancialData)

        if symbol:
            query_obj = query_obj.filter(FinancialData.symbol == symbol)
        if start_date:
            query_obj = query_obj.filter(FinancialData.date >= start_date)
        if end_date:
            query_obj = query_obj.filter(FinancialData.date <= end_date)
        total_cnt = query_obj.count()
        if page and limit:
            offset = (page - 1) * limit
            query_obj = query_obj.offset(offset).limit(limit)
        financial_data = query_obj.all()

        return total_cnt, financial_data
