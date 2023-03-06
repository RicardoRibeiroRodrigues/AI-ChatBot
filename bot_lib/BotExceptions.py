
class InvalidCrypto(Exception):
    def __init__(self, ticker: str):
        super().__init__(f'It seems that {ticker} is not in the database, please try again with a other crypto.')

class FetchError(Exception):
    def __init__(self):
        super().__init__(
            """Error fetching data from the api, please check the arguments or try again later.
                Tip: Check if the crypto existed in the given date range.
            """
        )