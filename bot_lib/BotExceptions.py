
class InvalidCrypto(Exception):
    def __init__(self, ticker: str, crypto_list: list[str]):
        error_msg = f'The crypto {ticker} is invalid!'
        self.valid_cryptos = crypto_list
        super().__init__(error_msg)
    
    def get_valid_cryptos(self) -> list[str]:
        return self.valid_cryptos

class FetchError(Exception):
    def __init__(self):
        super().__init__(
            """Error fetching data from the api, please check the arguments or try again later.
                Tip: Check if the crypto existed in the given date range.
            """
        )