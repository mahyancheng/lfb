import yfinance as yf
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
    AsyncCallbackManagerForToolRun,
)
from typing import Optional, Type

class StockSchema(BaseModel):
    ticker: str = Field(description="should be a valid stock ticker")

class StockTool(BaseTool):
    name = "stock_tool"
    description = "useful for when you need to get stock history and fundamentals"
    args_schema: Type[StockSchema] = StockSchema

    def _run(
        self,
        ticker: str,

        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        stock = yf.Ticker(ticker)
        history = stock.history(period="5d")
        info = stock.info
        # remove keys from the dictionary
        keys_to_remove = ['address1', 'city', 'state', 'zip', 'country', 'phone', 'fax', 'website', 'longBusinessSummary', 'companyOfficers', 'underlyingSymbol', 'firstTradeDateEpoch', 'timeZoneFullName', 'timeZoneShortName', 'messageBoardId', 'gmtOffSetMillliseconds', 'exchange', 'quoteType', 'governanceEpochDate', 'compensationAsOfEpochDate']
        for key in keys_to_remove:
            if key in info:
                del info[key]
        return {"fundamentals": info}
        return {"history": history, "fundamentals": info}

    async def _arun(
        self,
        ticker: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("stock_tool does not support async")