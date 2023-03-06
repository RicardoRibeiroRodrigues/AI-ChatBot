
class InvalidCrypto(Exception):
    def __init__(self, ticker: str):
        super().__init__(f'It seems that {ticker} is not in the database, please try again with a other crypto.')