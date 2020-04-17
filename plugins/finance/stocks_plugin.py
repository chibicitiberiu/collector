import datetime

from peewee import *
from playhouse.shortcuts import model_to_dict

import config
from database import BaseModel
from plugins.plugin import Plugin
import yfinance as yf


class Stocks(BaseModel):
    date = DateTimeField(index=True, default=datetime.datetime.now(), null=False)
    ticker = TextField(null=False)
    label = TextField(null=False)
    value_open = FloatField(null=False)
    value_close = FloatField(null=False)
    value_high = FloatField(null=False)
    value_low = FloatField(null=False)


class StocksPlugin(Plugin):
    models = [Stocks]

    def get_interval(self):
        return config.STOCKS_INTERVAL

    def execute(self):
        for ticker, label in config.STOCKS_TICKERS.items():
            # Get last existing date
            latest_date = Stocks.select(Stocks.date) \
                            .order_by(Stocks.date.desc()) \
                            .limit(1) \
                            .scalar()

            try:
                yfticker = yf.Ticker(ticker)

                if latest_date is None:
                    data = yfticker.history(period='max')
                else:
                    data = yfticker.history(start=latest_date + datetime.timedelta(seconds=1))

                for row in data.itertuples():
                    entry = Stocks()
                    entry.date = row.Index.to_pydatetime()
                    entry.ticker = ticker
                    entry.label = label
                    entry.value_open = row.Open
                    entry.value_close = row.Close
                    entry.value_high = row.High
                    entry.value_low = row.Low
                    entry.save()
                    print(model_to_dict(entry))
            except BaseException as e:
                print(e)