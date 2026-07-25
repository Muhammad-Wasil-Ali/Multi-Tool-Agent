from langchain_core.tools import BaseTool
from app.configs.keys_config import settings
from pydantic import BaseModel,Field
from typing import Type
import requests
from app.exception.custome_exceptions import CurrencyAPIError,InvalidCurrencyCodeError
from app.logger.custom_logger import get_logger
EXCHANGERATE_API_KEY=settings.EXCHANGERATE_API_KEY

logger=get_logger(__name__)
class ConverionRateSchema(BaseModel):
    base_currency:str=Field(description="This is the base currency from which we need to convert")
    target_currency:str=Field(description="This is the target currency in which we want to convert")


class CurrencyConverterSchema(BaseModel):
    base_currency:int=Field(description="This is the base currency which we need to convert")
    conversion_rate:float=Field(description="This is the conversion rate given by the rate_conversion tool")
    
class RateConversion(BaseTool):
    name:str="rate_conversion"
    description:str="This tool take base currency and target currency as input and get converion rate between the given currencies"
    args_schema:Type[ConverionRateSchema]=ConverionRateSchema
    
    
    def _run(self,base_currency:str,target_currency:str):
        
        
        url=f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base_currency}/{target_currency}"
        
        logger.info(f"Fetching conversion rate from {base_currency} -> {target_currency}")
        try:
            response=requests.get(url,timeout=10)
            response.raise_for_status()
            data=response.json()
            if data.get("result") != "success":
                logger.error(f"Invalid currency code: {base_currency} or {target_currency}")
                raise InvalidCurrencyCodeError(f"Invalid currency code: {base_currency} or {target_currency}")

            logger.info(f"Conversion rate fetched: 1 {base_currency} = {data['conversion_rate']} {target_currency}")
            return data

        except requests.exceptions.HTTPError as e:
            logger.error(f"Currency API HTTP error: {e}")
            raise CurrencyAPIError(f"Currency API error: {e}")
        
        except requests.exceptions.Timeout:
            logger.error("Currency API request timed out")
            raise CurrencyAPIError("Currency API request timed out.")

        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to currency API")
            raise CurrencyAPIError("Could not connect to currency API.")

        except requests.exceptions.RequestException as e:
            logger.error(f"Currency API request failed: {e}")
            raise CurrencyAPIError(f"Currency API request failed: {e}")
    


class CurrencyConvert(BaseTool):
    name:str="currency_converter"
    description:str="This tool accept the base currency as integer and conversion rate as input and convert the bse currency into target currency"
    args_schema:Type[CurrencyConverterSchema]=CurrencyConverterSchema
    
    
    def _run(self,base_currency:int,conversion_rate:float):
        logger.info(f"Converting curency from {base_currency} to target currency")
        return base_currency*conversion_rate
rate_conversion=RateConversion()
currency_converter=CurrencyConvert()
if __name__=="__main__":
    result=rate_conversion.invoke({"base_currency":"usd","target_currency":"pkr"})
    print(result)
    result2=currency_converter.invoke({"base_currency":10,"conversion_rate":result["conversion_rate"]})
    
    print(result2)