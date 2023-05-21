"""
Validators for Financial Data Queries

This module defines the validator classes for validating financial data query parameters
"""

from datetime import date, timedelta

from pydantic import BaseModel, validator


class BaseFinancialDataValidator(BaseModel):
    """
    Base validator class for validating query parameters
    """
    symbol: str = None
    end_date: date = None
    start_date: date = None

    @validator("start_date", pre=True)
    def parse_start_date(cls, value):
        if value is not None and not isinstance(value, date):
            return date.fromisoformat(value)
        return value

    @validator("end_date", pre=True)
    def parse_end_date(cls, value):
        if value is not None and not isinstance(value, date):
            return date.fromisoformat(value)
        return value

    @validator("start_date")
    def check_start_date_before_end_date(cls, value, values):
        if value and "end_date" in values and isinstance(values["end_date"], date) and value > values["end_date"]:
            raise ValueError("start_date must be before end_date")
        return value

    @validator("start_date")
    def check_start_date_before_tomorrow(cls, value):
        if value and value > date.today():
            raise ValueError("start_date cannot be later than today")
        return value

    @validator("end_date")
    def check_end_date_before_tomorrow(cls, value):
        if value and value > date.today():
            raise ValueError("end_date cannot be later than today")
        return value

    @validator("symbol")
    def check_valid_symbol(cls, value):
        if value and value not in ["AAPL", "IBM"]:
            raise ValueError('only "AAPL" or "IBM" is supported')
        return value


class GetFinancialDataValidator(BaseFinancialDataValidator):
    """
    Validator class for validating query parameters for retrieving financial data.
    """
    limit: int = 5
    page: int = 1

    @validator("limit")
    def check_limit(cls, value):
        if value < 1:
            raise ValueError("limit must be greater than or equal to 1")
        return value

    @validator("page")
    def check_page(cls, value):
        if value < 1:
            raise ValueError("page must be greater than or equal to 1")
        return value


class GetStatisticsValidator(BaseFinancialDataValidator):
    """
    Validator class for validating query parameters for calculating statistical data.
    """
    @validator("start_date", pre=True)
    def parse_start_date(cls, value):
        if value is None:
            raise ValueError("start_date is required")
        if not isinstance(value, date):
            return date.fromisoformat(value)
        return value

    @validator("end_date", pre=True)
    def parse_end_date(cls, value):
        if value is None:
            raise ValueError("end_date is required")
        if not isinstance(value, date):
            return date.fromisoformat(value)
        return value

    @validator("symbol")
    def check_valid_symbol(cls, value):
        if value is None:
            raise ValueError("symbol is required")
        if value not in ["AAPL", "IBM"]:
            raise ValueError('only "AAPL" or "IBM" is supported')
        return value

    # Unlike financial data api, it is better to limit the start_date and end_date within 14 days
    # to avoid returning misleading information
    @validator("start_date")
    def check_start_date_after_two_week_ago(cls, value):
        start_day = date.today() - timedelta(14)
        if value < start_day:
            raise ValueError(f"start_date should be greater than or equal to {start_day.strftime('%Y-%m-%d')}")
        return value

    @validator("end_date")
    def check_end_date_after_two_week_ago(cls, value):
        start_day = date.today() - timedelta(14)
        if value < start_day:
            raise ValueError(f"end_date should be greater than or equal to {start_day.strftime('%Y-%m-%d')}")
        return value
