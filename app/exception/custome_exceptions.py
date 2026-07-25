

class BaseAppException(Exception):
    """Base exception for this application."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class WeatherAPIError(BaseAppException):
    """Raised when the weather API call fails."""
    pass


class CityNotFoundError(WeatherAPIError):
    """Raised when the given city is not found."""
    pass


class CurrencyAPIError(BaseAppException):
    """Raised when the currency conversion API call fails."""
    pass


class InvalidCurrencyCodeError(CurrencyAPIError):
    """Raised when an invalid currency code is provided."""
    pass