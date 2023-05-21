"""
Financial Data Service

This module defines the `FinancialDataService` class,
which provides methods for retrieving financial data and calculating statistics based on the data.
"""
from datetime import date

from .repository import FinancialDataRepository


class FinancialDataService:
    """
    Financial Data Service

    This class provides methods for retrieving financial data and calculating statistics based on the data.
    """
    def __init__(self):
        self.financial_data_repository = FinancialDataRepository()

    def get_financial_data(self, symbol: str, start_date: date, end_date: date, limit: int, page: int) -> dict:
        """
        Retrieves financial data based on the specified query parameters.

        :param symbol: The symbol of the financial data to query.
        :param start_date: The start date of the date range to filter records.
        :param end_date: The end date of the date range to filter records.
        :param limit: The maximum number of records to return per page.
        :param page: The page number of the records to retrieve.
        :return: A dict containing the matched data, pagination info, and error info
        """
        result = {"data": [], "pagination": {}, "info": {"error": ""}}

        try:
            total_cnt, symbol_prices = self.financial_data_repository.get_financial_data_by_date_range(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                limit=limit,
                page=page
            )

            result["data"] = symbol_prices
            result["pagination"] = {
                "count": total_cnt,
                "page": page,
                "pages": total_cnt // limit,
                "limit": limit
            }
        except Exception as error:
            result["info"]["error"] = str(error)

        return result

    def get_statistics_data(self, symbol: str, start_date: date, end_date: date) -> dict:
        """
        Calculate statistical data based on the specified query parameters.

        :param symbol: The symbol of the financial data to query.
        :param start_date: The start date of the date range to filter records.
        :param end_date: The end date of the date range to filter records.
        :return: A dict containing the statistical data, and error info
        """
        result = {"data": {}, "info": {"error": ""}}

        try:
            total_cnt, quotes = self.financial_data_repository.get_financial_data_by_date_range(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date
            )

            result["data"] = {
                "symbol": symbol,
                "start_date": start_date,
                "end_date": end_date,
                "average_daily_open_price":
                    0 if total_cnt == 0 else round(sum(d.open_price for d in quotes) / total_cnt, 2),
                "average_daily_close_price":
                    0 if total_cnt == 0 else round(sum(d.close_price for d in quotes) / total_cnt, 2),
                "average_daily_volume":
                    0 if total_cnt == 0 else round(sum(d.volume for d in quotes) / total_cnt, 2),
            }
        except Exception as error:
            result["info"]["error"] = str(error)

        return result
