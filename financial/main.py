"""
FastAPI Application for Financial Data

This module implements a FastAPI application for retrieving and counting financial data.
It provides two APIs:
- GET /api/financial_data: retrieve financial data records that match the specified period and symbol
- GET /api/statistics: calculate the average daily open price, average daily close price, average daily volume
                       for the specified period

"""
from datetime import date

from fastapi import FastAPI
from pydantic import ValidationError
from .validator import GetFinancialDataValidator, GetStatisticsValidator

from .service import FinancialDataService


description = """
## Descriptions
This service is a prototype for the CTW take-home assignment. 
It is implemented in Python 3.11 and integrated with a MySQL database.

## APIs
### Retrieve records from financial_data
- Query prices by symbols.
- Symbols may be either **AAPL** or **IBM**.
- The date range for **start_date** and **end_date** must be a date before today, and **start_date** must be before **end_date**.
- The date format should be YYYY-MM-DD, e.g., 2023-01-01.
- Pagination is implemented.

### Get statistics of financial_data
- Query prices by symbols.
- Symbols may be either **AAPL** or **IBM**.
- The date range for **start_date** and **end_date** must be a date before today, and **start_date** must be before **end_date**.
- The date format should be YYYY-MM-DD, e.g., 2023-01-01.
"""

tags_metadata = [
    {
        "name": "Get financial data",
        "description": "Retrieve financial data records that match the specified period and symbol",
    },
    {
        "name": "Get statistical data",
        "description": "Calculate the average daily open price, average daily close price, average daily volume \
                       for the specified period",
    },
]

app = FastAPI(
    title="CTW Take-Home Assignment",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata,
)


@app.get("/api/financial_data", tags=["Get financial data"])
async def financial_data(
    symbol: str = None,
    start_date: str = None,
    end_date: str = None,
    limit: int = 5,
    page: int = 1,
) -> dict:
    """
    This function is an API endpoint that retrieves financial data based on the specified query parameters.

    :param symbol: The symbol of the financial data to query.
    :param start_date: The start date of the date range to filter records.
    :param end_date: The end date of the date range to filter records.
    :param limit: The maximum number of records to return per page.
    :param page: The page number of the records to retrieve.
    :return: The financial data that matches the specified query parameters.
    """
    try:
        query_params = GetFinancialDataValidator(
            symbol=symbol,
            end_date=end_date,
            start_date=start_date,
            limit=limit,
            page=page,
        )
        financial_data_service = FinancialDataService()
        return financial_data_service.get_financial_data(
            symbol=query_params.symbol,
            start_date=query_params.start_date,
            end_date=query_params.end_date,
            limit=query_params.limit,
            page=query_params.page,
        )
    except ValidationError as e:
        return parse_error_response(e)


@app.get("/api/statistics", tags=["Get statistical data"])
async def statistics(symbol: str = None, start_date: date = None, end_date: date = None) -> dict:
    """
    This function is an API endpoint that calculate statistical data based on the specified query parameters.

    :param symbol: The symbol of the financial data to query.
    :param start_date: The start date of the date range to filter records.
    :param end_date: The end date of the date range to filter records.

    :return: The statistical data that matches the specified query parameters.
    """
    try:
        financial_data_service = FinancialDataService()
        query_params = GetStatisticsValidator(symbol=symbol, end_date=end_date, start_date=start_date)
        return financial_data_service.get_statistics_data(
            symbol=query_params.symbol,
            start_date=query_params.start_date,
            end_date=query_params.end_date
        )
    except ValidationError as e:
        return parse_error_response(e)


def parse_error_response(e: ValidationError) -> dict:
    """
    This function parses a `ValidationError` and generates an error response.

    :param e: The `ValidationError` instance to parse.
    :return: A dictionary representing the error response.
    """
    result = {"data": [], "pagination": {}, "info": {"error": []}}
    error_messages = []
    for error in e.errors():
        error_messages.append(error["msg"])
    result["info"]["error"] = error_messages
    return result
