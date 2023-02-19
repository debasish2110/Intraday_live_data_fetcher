
#### importing dependencies ####

import requests
import time
import pandas as pd
import json
from datetime import datetime


######## code ########

class TradeHandler(Exception):
    pass

class Trade(object):
    def __init__(self) -> None:
        self.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }

    def convert_to_ts(self, date):
        tt = date.timetuple()
        return round(time.mktime(tt))

    def convert_to_date(self, date_ts):
        return datetime.fromtimestamp(date_ts)

    def fix_datetime_in_dataframe(self, dataframe):
        try:
            ts = dataframe['Date-Time']
            dataframe = dataframe.drop('Date-Time', axis=1)
            date = [{'Date-Time': self.convert_to_date(dt)} for dt in ts]
            new_dataframe = pd.concat([pd.DataFrame(date), dataframe], axis=1)
            return new_dataframe
        except Exception as e:
            raise TradeHandler(f'Error occured while fixing date time: {e}')


    def get_response_from_site(self, url_to_fetch, fetch_dictionary=False):
        try:
            resp = requests.get(url_to_fetch, headers=self.headers)
            if fetch_dictionary:
                return json.load(resp.json())

            return resp.json()
        except Exception as e:
            raise TradeHandler(f'Some error occured while geting the response: {e}')

    def resp_to_dataframe(self, url_to_fetch):
        response_json = self.get_response_from_site(url_to_fetch)
        df = pd.DataFrame(response_json).rename(
            columns={'t': 'Date-Time', 'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'close', 'v': 'Volume'}
            )
        
        df = self.fix_datetime_in_dataframe(df)
        return df


####### Code Flow #######

if __name__ == '__main__':
    trader = Trade()

    # hardcoding for now, will remove hardcoding later.
    start_time = trader.convert_to_ts(datetime(2023, 2, 19))
    end_time = trader.convert_to_ts(datetime(2023, 2, 18))
    url_to_fetch = f'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol=RELIANCE&resolution=5&from={start_time}&to={end_time}&countback=329&currencyCode=INR'
    data_frame = trader.resp_to_dataframe(url_to_fetch)
    print(data_frame)

    