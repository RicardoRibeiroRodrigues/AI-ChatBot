import aiohttp
import plotly.graph_objects as go
import asyncio
import re
import datetime
import json
from .BotExceptions import InvalidCrypto, FetchError

class ApiInterface:
    BASE_URL = 'https://api.coincap.io/v2/assets'
    
    def __init__(self, api_key) -> None:
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }
        with open('data/assets.json', 'r') as f:
            self.assets = json.load(f)
        
    
    def validate_symbol(self, symbol: str) -> bool:
        exp = r'^[A-Za-z]{2,5}'
        return re.fullmatch(exp, symbol) is not None
    
    def validate_interval(self, interval: str) -> bool:
        exp = r'\d{4}-\d{1,2}-\d{1,2}\.\d{4}-\d{1,2}-\d{1,2}'
        return re.fullmatch(exp, interval) is not None

    def create_graph(self, data: dict, asset_id: str) -> str:
        # Create a graph of the data
        x = []
        y = []
        for d in data:
            y.append(float(d['priceUsd']))
            x.append(datetime.datetime.fromtimestamp(d['time'] / 1e3))
        
        fig = go.Figure(data=go.Scatter(x=x, y=y))

        fig.update_layout(
            title=f'{asset_id.capitalize()} price over time',
            xaxis_title='Date',
            yaxis_title='Price [USD]',
            title_x=0.5,
            template='plotly_dark',
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            xaxis=dict(gridcolor='gray'),
            yaxis=dict(gridcolor='gray'),
            margin=dict(l=70, r=30, t=50, b=50),
        )
        path = f'{asset_id}.png'
        fig.write_image(path, width=800, height=600, scale=3)
        return path
        


    async def fetch_data(self, ticker: str, start_date: datetime=None, end_date: datetime=None) -> tuple:
        asset_id = self.assets.get(ticker.upper())
        if asset_id is None:
            raise InvalidCrypto(ticker, self.assets.keys())

        date_arg = ""
        if start_date and end_date:
            # Datetime to unix timestamp in milliseconds (api requirement)
            start_date = start_date.replace(tzinfo=datetime.timezone.utc).timestamp() * 1e3
            end_date = end_date.replace(tzinfo=datetime.timezone.utc).timestamp() * 1e3
            date_arg = f'&start={int(start_date)}&end={int(end_date)}'

        url_historical = f'{self.BASE_URL}/{asset_id}/history?interval=d1{date_arg}'
        url_basic_info = f'{self.BASE_URL}/{asset_id}'
        
        hist_data, basic_info = await self.get_all_data(url_basic_info, url_historical)
        graph_path = self.create_graph(hist_data, asset_id)
        return (basic_info, graph_path)


    async def get_all_data(self, info_url: str, historical_url: str) -> tuple:
        # Make two requests and wait for the two of them to finish
        # before returning the result
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                tasks = (
                    asyncio.ensure_future(self._get(session, historical_url)),
                    asyncio.ensure_future(self._get(session, info_url))
                )

                historical_data, resume_data = await asyncio.gather(*tasks)
            except Exception:
                raise FetchError()
            
        return (historical_data, resume_data)

    async def _get(self, session, url: str) -> dict:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f'Error fetching data from {url}')
        
            resp = await resp.json()
            if 'error' in resp:
                raise Exception(resp['error'])
            return resp['data']

if __name__ == '__main__':
    api_inter = ApiInterface("")
    asyncio.run(api_inter.fetch_data('bitcoin', datetime.datetime(2020, 1, 1), datetime.datetime(2020, 12, 31)))